"""
Python script to load data from multiple csv files with custom mapping.

"""


# load required packages
import os
import pandas as pd
from sqlalchemy import create_engine
from mapping import file_table_column_map # importing custom mapping

# PostgreSQL connection 
engine = create_engine('postgresql+psycopg2://postgres:1995@localhost:5432/faostat_ms_dsci_project')

# path to the directory containing cleaned CSV files which are to be loaded
data_folder = '/Users/gurjitsingh/Desktop/MS Data Science/MS_Project_Python/cleaned_datasets'

# Loop through each file in the mapping
for csv_file, config in file_table_column_map.items():
    file_path = os.path.join(data_folder, csv_file)
    table = config['table']
    col_map = config['column_mapping']

    try: 
        df = pd.read_csv(file_path)

        # rename columns
        df.rename(columns=col_map, inplace=True)

        # reorder to match DB table column order
        df = df[list(col_map.values())]

        # load into DB
        df.to_sql(table, engine, if_exists='append', index=False)

        print(f"Loaded '{csv_file}' into '{table}'")
    except Exception as e:
        print(f"Error loading '{csv_file}': {e}")