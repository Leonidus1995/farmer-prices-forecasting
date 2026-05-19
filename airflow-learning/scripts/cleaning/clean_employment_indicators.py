# Load required libraries
import pandas as pd

# Define constants
DESIRED_INDICATORS = [
    'Total employment in agrifood systems (AFS)',
    'Share of AFS employment in total employment',
    'Agriculture value added per worker (constant 2015 US$)',
    'Employment in agriculture - ILO modelled estimates',
    'Share of employment in agriculture in total employment - ILO Modelled Estimates',
]

DESIRED_SEX = "Total" # out of three- 'Total', 'Male', and 'Female'

REQUIRED_COLUMNS = ["Area Code", "Area", "Year Code", "Year", "Indicator", 
                    "Sex", "Value"]

# Actual cleaning/transformation function
def clean_employment_indicators(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform FAOSTAT Employment Indicators data into a country-year feature table
    """
    data = raw_data.copy()

    # Verify for all required columns
    missing_cols = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_cols:
        raise ValueError(f"Missing required columns: {sorted(missing_cols)}")

    # Verify for all required indicators
    available_indicators = data['Indicator'].dropna().unique()
    missing_indicators = set(DESIRED_INDICATORS) - set(available_indicators)

    if missing_indicators:
        raise ValueError(f"Missing desired indicators: {sorted(missing_indicators)}")

    # Filter raw dataset
    filtered_data = data.loc[
        (data['Indicator'].isin(DESIRED_INDICATORS)) &
        (data['Sex'] == DESIRED_SEX)
    ]

    # Verify for empty filtered dataset
    if len(filtered_data) == 0:
        raise ValueError("There are no rows in the filtered dataset.")
    
    # Verify for duplicated rows
    num_duplicates = filtered_data.duplicated(
        subset=['Area Code', 'Area', 'Year Code', 'Year', 'Indicator'], 
        keep=False
        ).sum()
    
    # Use strict pivot only after confirming one value per country-year-indicator
    if num_duplicates == 0:
        pivoted_data = filtered_data.pivot(
            index=['Area Code', 'Area', 'Year Code', 'Year'],
            columns="Indicator",
            values="Value"
        ).reset_index()

        pivoted_data.columns.name = None

    else:
        raise ValueError("There are duplicate rows in the filtered dataset.")

    # Rename the columns and return final cleaned dataset
    cleaned_data = pivoted_data.rename(
        columns= {
            'Area Code': 'area_code',
            'Area': 'area',
            'Year Code': 'year_code',
            'Year': 'year',
            'Agriculture value added per worker (constant 2015 US$)': 'value_added_per_worker',
            'Employment in agriculture - ILO modelled estimates': 'employment_in_agriculture',
            'Share of employment in agriculture in total employment - ILO Modelled Estimates': 'agri_employment_share_in_total_employment',
            'Total employment in agrifood systems (AFS)': 'total_employment_afs',
            'Share of AFS employment in total employment': 'afs_employment_share_in_total_employment'
        }
    )

    return cleaned_data


    

    

    
