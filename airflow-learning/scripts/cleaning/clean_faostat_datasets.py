# 1. IMPORTS
from pathlib import Path
from dataclasses import dataclass
from typing import Callable
import pandas as pd
import zipfile

# 2. PATHS AND CONSTANTS
PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_DATA_FOLDER = PROJECT_ROOT / "raw_datasets" / "faostat_bulk"
PROCESSED_DATA_FOLDER = PROJECT_ROOT / "processed_datasets" / "cleaned_datasets"



# 3. DatasetConfig DATACLASS
@dataclass
class DatasetConfig:
    """
    Defines a configuration object for one dataset.
    One of its fields is a function that takes a pandas DF as input and outputs a 
    cleaned pandas DF.
    """
    name: str
    zip_filename: str
    output_filename: str
    cleaning_function: Callable[[pd.DataFrame], pd.DataFrame]


# 4. DATASET SPECIFIC CLEANING FUNCTION
from scripts.cleaning.clean_producer_prices import clean_producer_prices

# 5. SHARED HELPER FUNCTIONS
def read_raw_zip(zip_filename: str) -> pd.DataFrame:
    """
    Extracting and reading data from input zip file.
    """
    input_zip_path = INPUT_DATA_FOLDER / zip_filename

    if not input_zip_path.exists():
        raise FileNotFoundError(f"Input zip file ({zip_filename}) does not exists at {input_zip_path}.")

    with zipfile.ZipFile(input_zip_path, "r") as z:
        file_list = z.namelist()

        csv_files = [f for f in file_list if f.endswith('.csv')]

        main_csv_files = [f for f in csv_files if 'All_Data' in f]

        if len(main_csv_files) == 0:
            raise ValueError(f"There is no main 'All_Data' csv file in {zip_filename}.")
        if len(main_csv_files) > 1:
            raise ValueError(f"There are multiple main 'All_Data' csv files in {zip_filename}.")
        
        main_csv = main_csv_files[0]
        with z.open(main_csv) as file:
            df = pd.read_csv(file, low_memory=False)

    return df

def write_cleaned_data(data: pd.DataFrame, output_file_path: Path) -> None:
    """
    Writing cleaned data to a csv file.
    """
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_file_path, index=False)


# 6. DATASETS CONFIG LIST
DATASETS = [
    DatasetConfig(
        name="producer_prices",
        zip_filename="Prices_E_All_Data_(Normalized).zip",
        output_filename="producer_prices_cleaned.csv",
        cleaning_function=clean_producer_prices
    )
]

# 7. ORCHESTRATION LOGIC


# 8. MAIN FUNCTION