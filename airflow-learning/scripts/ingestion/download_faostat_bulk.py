import requests
from pathlib import Path
import xml.etree.ElementTree as ET
import csv
from datetime import datetime

FAOSTAT_DATASETS = [
    "Climate_change_Emissions_indicators_E_All_Data_(Normalized)",
    "Environment_Cropland_nutrient_budget_E_All_Data_(Normalized)",
    "Employment_Indicators_Agriculture_E_All_Data_(Normalized)",
    "FertilizersNutrient_E_All_Data_(Normalized)",
    "Investment_CreditAgriculture_E_All_Data_(Normalized)",
    "Investment_ForeignDirectInvestment_E_All_Data_(Normalized)",
    "Investment_GovernmentExpenditure_E_All_Data_(Normalized)",
    "LandUse_E_All_Data_(Normalized)",
    "Macro-Statistics_Key_Indicators_E_All_Data_(Normalized)",
    "Pesticides_Trade_E_All_Data_(Normalized)",
    "Pesticides_Use_E_All_Data_(Normalized)",
    "Population_E_All_Data_(Normalized)",
    "Prices_E_All_Data_(Normalized)",
    "Production_Crops_Livestock_E_All_Data_(Normalized)",
    "Production_Indices_E_All_Data_(Normalized)",
    "Temperature_change_E_All_Data_(Normalized)",
    "Trade_CropsLivestock_E_All_Data_(Normalized)",
    "Trade_CropsLivestockIndicators_E_All_Data_(Normalized)",
    "Trade_Indices_E_All_Data_(Normalized)",
    "Value_of_Production_E_All_Data_(Normalized)",
    ]

FAOSTAT_CATALOG_URL = "https://bulks-faostat.fao.org/production/datasets_E.xml"


def fetch_catalog_xml(catalog_url: str) -> ET.Element:
    """
    Fetch FAOSTAT bulk download XML catalog, and parse it into an XML tree.

    Parameters: 
        catalog_url: URL of the FAOSTAT bulk download XML file.

    Returns:
        catalog_root: Root element of the parsed XML tree.
    """

    response = requests.get(catalog_url, timeout=30)
    response.raise_for_status()

    return ET.fromstring(response.content)



def catalog_to_records(catalog_root: ET.Element) -> list[dict]:
    """
    Convert FAOSTAT catalog XML elements into a list of dataset records.

    Parameters:
        catalog_root: Root element of the parsed XML tree.

    Returns:
        records: List of dictionaries, where each dictionary represents one dataset
        and contains key-value pairs derived from XML child tags (e.g., FileLocation,
        FileSize, FileRows, DateUpdate).
    """

    catalog_records = []

    for dataset in catalog_root:
        record = {}

        for element in dataset:
            record[element.tag] = element.text

        catalog_records.append(record)

    return catalog_records



def match_required_datasets(required_datasets, catalog_records):
    """
    Match required FAOSTAT dataset name against FileLocation URLs in the 
    FAOSTAT bulk download catalog.

    Parameters: 
        required_datasets: list of required FAOSTAT dataset name strings.
        catalog_records: list of dictionaries parsed from the FAOSTAT XML catalog.

    Returns:
        matched_datasets: list of dictionaries containing dataset_name, url, 
        DateUpdate, FileSize, and FileRows for each matched dataset.

        missing_datasets: list of required dataset names not found in the catalog.
    """

    matched_datasets = []
    missing_datasets = []

    for dataset in required_datasets:
        found = False

        for record in catalog_records:
            if dataset in record.get('FileLocation', ""):
                matched_datasets.append({
                    'dataset_name': dataset,
                    'url': record.get('FileLocation'),
                    'date_update': record.get('DateUpdate'),
                    'file_size_catalog': record.get('FileSize'),
                    'file_rows': record.get('FileRows')
                })
                found = True
                break

        if not found:   
            missing_datasets.append(dataset)

    return matched_datasets, missing_datasets


def download_file(url, output_dir, overwrite=False):
    """
    Download the required FAOSTAT data file from the given URL to the specified 
    directory.

    Parameters:
        url: URL of the file to download.
        output_dir: Directory where the file will be saved.
        overwrite: If False, skip download if the file already exists.
                   If True, re-download and replace the existing file. 

    Returns:
        file_path: Path to the final downloaded (or existing) file.

    Behavior:
        - Ensures the file is fully downloaded before returning.
        - Raises an exception if download fails.
    """

    filename = url.split('/')[-1]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    if output_path.exists() and not overwrite:
        print("File already exists. Skipping download.")
        return output_path

    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    temp_path = output_path.with_suffix(".temp")

    with open(temp_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                file.write(chunk)

    temp_path.rename(output_path)

    return output_path


def write_manifest(rows, manifest_path):
    """
    Write FAOSTAT ingestion run metadata to a CSV manifest.

    Parameters:
        rows: List of dictionaries, where each dictionary represents one dataset
              attempted during the ingestion run. Expected keys include run_id,
              dataset_name, file_name, url, date_update, file_size_catalog,
              local_path, downloaded_at, status, and error_message.

        manifest_path: Path where the manifest CSV should be written.

    Returns:
        manifest_path: Path to the saved manifest CSV.

    Behavior:
        Creates the parent manifest directory if needed.
        Writes one row per dataset attempt.
        Overwrites the manifest for the current run.
    """

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(manifest_path, 'w', newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "run_id", "dataset_name", "file_name", "url", "date_update", 
                "file_size_catalog", "local_path", "downloaded_at", "status", 
                "error_message"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


def main():
    """
    Orchestrate FAOSTAT bulk data ingestion workflow.
    """

    # Step1: SET PATHS

    ## Find the project root by walking up two directories, relative to the current file
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    ## Create directories to store downloaded FAOSTAT data files
    RAW_DATA_DIR = PROJECT_ROOT / "raw_datasets"

    FAOSTAT_BULK_DIR = RAW_DATA_DIR / "faostat_bulk"
    FAOSTAT_BULK_DIR.mkdir(parents=True, exist_ok=True)

    MANIFEST_DIR = RAW_DATA_DIR / "metadata"
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    # Step2: FETCH FAOSTAT BULK DOWNLOAD CATALOG
    root = fetch_catalog_xml(catalog_url=FAOSTAT_CATALOG_URL)

    # Step3: PARSE RECORDS
    catalog_records = catalog_to_records(catalog_root=root)

    # Step4: MATCH DATASETS
    matched_datasets, missing_datasets = match_required_datasets(
        required_datasets=FAOSTAT_DATASETS, 
        catalog_records=catalog_records
        )
    
    if missing_datasets:
        missing_text = "\n".join(f"- {dataset}" for dataset in missing_datasets)
        raise ValueError(
            f"Missing required FAOSTAT datasets:\n{missing_text}\n"
            "Stopping ingestion. Check whether FAOSTAT changed file names."
        )

    # Step5: DOWNLOAD DATASETS AND WRITE MANIFEST
    run_id = datetime.now().strftime("%Y%m%dT%H%M%S")
    manifest_rows = []

    for dataset in matched_datasets:
        try:
            out_path = download_file(
                url=dataset['url'], 
                output_dir=FAOSTAT_BULK_DIR, 
                overwrite=True
                )
            
            manifest_rows.append({
                "run_id": run_id, 
                "dataset_name": dataset['dataset_name'], 
                "file_name": Path(dataset["url"]).name, 
                "url": dataset['url'], 
                "date_update": dataset['date_update'], 
                "file_size_catalog": dataset['file_size_catalog'], 
                "local_path": str(out_path), 
                "downloaded_at": datetime.now().isoformat("T", timespec="seconds"), 
                "status": "success", 
                "error_message": None
            })
            
        except Exception as Error:
            manifest_rows.append({
                "run_id": run_id, 
                "dataset_name": dataset['dataset_name'], 
                "file_name": Path(dataset["url"]).name, 
                "url": dataset['url'], 
                "date_update": dataset['date_update'], 
                "file_size_catalog": dataset['file_size_catalog'], 
                "local_path": None, 
                "downloaded_at": datetime.now().isoformat("T", timespec="seconds"), 
                "status": "failed", 
                "error_message": str(Error)
            })

    write_manifest(
        rows=manifest_rows, 
        manifest_path=MANIFEST_DIR / f"faostat_download_manifest_{run_id}.csv"
        )

    # Error message for Airflow to log
    if any(row['status']=='failed' for row in manifest_rows):
        raise ValueError("One or more FAOSTAT downloads failed. Check manifest.")
    
if __name__ == "__main__":
    main()


    
    


    




