import pandas as pd

REQUIRED_COLUMNS = [
    'Area Code','Area','Item Code','Item','Year','Year Code',
    'Element', 'Value'
    ]

FILTER_YEAR = 1990

ELEMENTS_TO_REMOVE = [
    'Stocks', 'Producing Animals/Slaughtered', 'Laying', 
    'Yield/Carcass Weight', 'Milk Animals'
    ]

def clean_crop_production(raw_data: pd.DataFrame) -> pd.DataFrame:
    data = raw_data.copy()

    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns.unique())
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    
    filtered_data = data.loc[
        (~data['Element'].isin(ELEMENTS_TO_REMOVE)),
        REQUIRED_COLUMNS
    ]

    duplicate_rows = filtered_data.duplicated(
        subset=['Area Code','Area','Item Code','Item','Year','Year Code'],
        keep=False
        ).sum()
    
    if duplicate_rows == 0:
        pivoted_data = filtered_data.pivot(
            index=['Area Code','Area','Item Code','Item','Year','Year Code'],
            columns='Element',
            values='Value'
        ).reset_index()
    else:
        raise ValueError("There are duplicate rows in the filtered data.")
    
    cleaned_data = pivoted_data.rename(
        columns = {
            'Area Code': 'area_code', 
            'Area': 'area', 
            'Item Code': 'item_code', 
            'Item': 'item', 
            'Year': 'year', 
            'Year Code': 'year_code',
            'Area harvested': 'area_harvested', 
            'Production': 'production', 
            'Yield': 'yield'
        }
    )

    return cleaned_data


