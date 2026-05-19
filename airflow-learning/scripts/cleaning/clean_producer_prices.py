from pathlib import Path
import zipfile
import pandas as pd 

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / 'raw_datasets' / 'faostat_bulk'
PROCESSED_DATA_DIR = PROJECT_ROOT / 'processed_datasets' / 'faostat_cleaned'
PRODUCER_PRICES_ZIP = RAW_DATA_DIR / 'Prices_E_All_Data_(Normalized).zip'
OUTPUT_PATH = PROCESSED_DATA_DIR / 'producer_prices_cleaned.csv'

# columns to drop
cols_to_drop = [
    "Area Code (M49)", "Item Code (CPC)", "Element Code",
    'Months', 'Months Code', 'Unit', 'Flag'
    ]

# elements to drop
elements_to_drop = ['Producer Price (LCU/tonne)', 'Producer Price (SLC/tonne)']

# items to drop
items_to_drop = [
    'Meat of other domestic camelids, fresh or chilled',
    'Meat of other domestic camelids, fresh or chilled (biological)',
    'Other pome fruits', 'Other sugar crops n.e.c.',
    'Meat of pigeons and other birds n.e.c., fresh, chilled or frozen (biological)',
    'Meat of pigeons and other birds n.e.c., fresh, chilled or frozen',
    'Meat of other domestic rodents, fresh or chilled',
    'Meat of other domestic rodents, fresh or chilled (biological)',
    'Other meat of mammals, fresh or chilled',
    'Edible roots and tubers with high starch or inulin content, n.e.c., fresh',
    'Other tropical fruits, n.e.c.', 'Other berries and fruits of the genus vaccinium n.e.c.',
    'Other fibre crops, raw, n.e.c.', 'Other oil seeds, n.e.c.',
    'Other stimulant, spice and aromatic crops, n.e.c.',
    'Fibre Crops Primary', 'Other citrus fruit, n.e.c.', 
    'Other nuts (excluding wild edible nuts and groundnuts), in shell, n.e.c.',
    'Eggs from other birds in shell, fresh, n.e.c.', 
    'Other stone fruits', 'Other vegetables, fresh n.e.c.', 
    'Other pulses n.e.c.', 'Cereals n.e.c.', 'Other fruits, n.e.c.'
    ]


def read_faostat_zip(zip_path: Path) -> pd.DataFrame:
    """
    Extracting and reading Producer price raw data from the input ZIP
    """
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file does not exist at {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as z:
        file_list = z.namelist()

        csv_files = [f for f in file_list if f.endswith('.csv')]

        main_csv_files = [
            f for f in csv_files 
            if "All_Data" in f
        ]

        if len(main_csv_files) == 0:
            raise ValueError(f"No main All_Data CSV found in {zip_path}")
        
        if len(main_csv_files) > 1:
            raise ValueError(f"Multiple All_Data CSV files found in {zip_path}")

        main_csv = main_csv_files[0]
        with z.open(main_csv) as file:
            df = pd.read_csv(file, low_memory=False)
        
    return df


def clean_producer_prices(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning and transforming the Producer Price raw data 
    """

    data = raw_data.copy()

    # filter the data to obtain desired rows (annual Producer prices)
    annual_data = data.loc[data['Months'] == 'Annual value'].copy()

    # drop irrelevant columns
    filtered_data = annual_data.drop(cols_to_drop, axis=1)

    # reshape the data frame from long to wide format
    pivoted_data = filtered_data.pivot_table(
        index = ["Area Code", "Area", "Item Code", "Item", "Year", "Year Code"],
        columns = 'Element',
        values = 'Value'
    )
    pivoted_data = pivoted_data.reset_index()
    pivoted_data.columns.name = None

    # drop un-desired columns from pivoted data frame
    reduced_data = pivoted_data.drop(elements_to_drop, axis = 1)

    # finding items with fewer than 100 rows of data
    item_counts = reduced_data['Item'].value_counts()
    sparse_items = item_counts.loc[item_counts < 100].index.to_list()

    # finding countries with fewer than 100 rows of data
    country_counts = reduced_data['Area'].value_counts()
    sparse_countries = country_counts.loc[
        country_counts < 100
        ].index.to_list()

    items_to_remove = list(set(items_to_drop + sparse_items))

    # dropping undesired items and countries
    desired_data = reduced_data.loc[
        (~reduced_data['Area'].isin(sparse_countries)) &
        (~reduced_data['Item'].isin(items_to_remove)), 
        :
    ]

    # Finding rows where both PPI and PP are missing and dropping them
    both_price_columns_missing = (
        (desired_data['Producer Price Index (2014-2016 = 100)'].isna()) &
        (desired_data['Producer Price (USD/tonne)'].isna())
        )

    cleaned_data = desired_data.loc[~both_price_columns_missing].copy()

    # Renaming columns
    cleaned_pp_df = cleaned_data.rename(
        columns={
            'Area Code': 'area_code', 
            'Area': 'area', 
            'Item Code': 'item_code', 
            'Item': 'item', 
            'Year': 'year', 
            'Year Code': 'year_code',
            'Producer Price (USD/tonne)': 'producer_price_usd_per_tonne', 
            'Producer Price Index (2014-2016 = 100)': 'producer_price_index'
        }
    )

    return cleaned_pp_df


def write_cleaned_data(data: pd.DataFrame, output_path: Path) -> None:
    """
    Write cleaned dataframe to CSV
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)


def main() -> None:
    """
    Orchestrate Producer Price data cleaning workflow.
    """

    raw_df = read_faostat_zip(zip_path = PRODUCER_PRICES_ZIP)
    cleaned_df = clean_producer_prices(raw_data = raw_df)
    write_cleaned_data(data = cleaned_df, output_path = OUTPUT_PATH)

    print("Producer prices data cleaning completed.")
    print(f"Number of rows: {cleaned_df.shape[0]}")
    print(f"Number of columns: {cleaned_df.shape[1]}")
    print(f"Output path: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()