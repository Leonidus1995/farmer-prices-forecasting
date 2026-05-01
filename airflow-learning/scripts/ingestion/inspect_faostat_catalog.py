from pathlib import Path
import requests
import xml.etree.ElementTree as ET    # XML parser
from datetime import datetime
import csv

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

## Find the project root by walking up two directories, relative to the current file
PROJECT_ROOT = Path(__file__).resolve().parents[2]

## create directories for storing data files
RAW_DATA_DIR = PROJECT_ROOT / "raw_datasets"

FAOSTAT_BULK_DIR = RAW_DATA_DIR / "faostat_bulk"
FAOSTAT_BULK_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_DIR = RAW_DATA_DIR / "metadata"
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)


print("Project root directory:", PROJECT_ROOT)
print("FAOSTAT bulk folder:", FAOSTAT_BULK_DIR)
print("Number of datasets requested:", len(FAOSTAT_DATASETS))
print("Created/verified raw data folders.")

######################### INSPECT FAOSTAT BULK CATALOG ##########################

FAOSTAT_CATALOG_URL = "https://bulks-faostat.fao.org/production/datasets_E.xml"

def fetch_catalog_xml(url: str):
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # stops the script if request failed
    return ET.fromstring(response.content) # parses XML into a python object


catalog_root = fetch_catalog_xml(FAOSTAT_CATALOG_URL)
print("Catalog root tag:", catalog_root.tag)
print("Number of child records:", len(catalog_root))


#for child in list(catalog_root[:3]):
    #print("\nRecord tag:", child.tag)
    #for element in child:
        #print(f" {element.tag}: {element.text}")

def catalog_to_records(catalog_root: ET.Element) -> list[dict]:
    records = []

    for dataset in catalog_root:
        record = {}

        for element in dataset:
            record[element.tag] = element.text

        records.append(record)

    return records

catalog_records = catalog_to_records(catalog_root)

print("\nFirst 2 catalog records as dictionaries:")
print(catalog_records[:2])

################## MATCH REQUIRED DATASETS WITH CATALOG ####################

matched_datasets = []
unmatched_datasets = []

catalog_files = []
for record in catalog_records:
    if record.get("FileLocation"):
        catalog_files.append(record.get("FileLocation"))

catalog_files = set(catalog_files)  

for dataset in FAOSTAT_DATASETS:
    matching_file = next(
        (file for file in catalog_files if dataset in file),
        None
    )
    if matching_file:
        matched_datasets.append({
            "dataset_name": dataset,
            "url": matching_file
        })
    else:
        unmatched_datasets.append(dataset)

if set(item['dataset_name'] for item in matched_datasets) == set(FAOSTAT_DATASETS):
    print("All required FAOSTAT datasets are present in the catalog.")

print("Matched datasets:")
for item in matched_datasets:
    print(item)

print("\nUn-matched datasets:")
for item in unmatched_datasets:
    print(item)


############## DOWNLOADING FAOSTAT DATASETS & SAVING MANIFEST #################

def download_faostat(url: str, output_dir: Path, overwrite: bool = False) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = url.split("/")[-1]
    output_path = output_dir / filename

    # skip if already exists
    if output_path.exists() and not overwrite:
        print(f"Skipping (already exists): {filename}")
        return output_path
    
    print(f"Downloading: {filename}")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # writing file in chunks
    with open(output_path, "wb") as file: # zip files are binary
        for chunk in response.iter_content(chunk_size=8192): # 8192 bytes = 8 KB
            if chunk:
                file.write(chunk)

    print(f"Saved to: {output_path}")

    return output_path

manifest_rows = []
for dataset in matched_datasets:
    try:
        path = download_faostat(
            url=dataset['url'],
            output_dir=FAOSTAT_BULK_DIR,
            overwrite = False
            )
        
        manifest_rows.append({
            "dataset_name": dataset['dataset_name'],
            "url": dataset['url'],
            "local_path": str(path),
            "downloaded_at": datetime.now().isoformat(timespec='seconds'),
            "status": 'success'
        })

    except Exception as error:
        manifest_rows.append({
            "dataset_name": dataset['dataset_name'],
            "url": dataset['url'],
            "local_path": None,
            "downloaded_at": datetime.now().isoformat(timespec='seconds'),
            "status": f"failed: {error}"
        })

manifest_path = MANIFEST_DIR / "faostat_download_manifest.csv"

with open(manifest_path, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "dataset_name",
            "url",
            "local_path",
            "downloaded_at",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(manifest_rows)

print(f"\nManifest written to: {manifest_path}")
