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



"""
Python script to load data from modified credit_to_agri.csv file. I previously 
loaded this csv file but had to modify it to include a new column called 'total_credit',
so I have to delete the previous table and loaded the modified version again.

This code chunk need not to be run separately if the code block above is already run.

"""
# load required packages
import os
import pandas as pd
from sqlalchemy import create_engine
from mapping import file_table_column_map # importing custom mapping

# PostgreSQL connection 
engine = create_engine('postgresql+psycopg2://postgres:1995@localhost:5432/faostat_ms_dsci_project')

# path to the directory containing cleaned CSV files which are to be loaded
file_path = '/Users/gurjitsingh/Desktop/MS Data Science/MS_Project_Python/cleaned_datasets/credit_to_agri_forestry_fishery_cleaned.csv'


desired_item = file_table_column_map['credit_to_agri_forestry_fishery_cleaned.csv']

table = desired_item['table']
col_map = desired_item['column_mapping']

df = pd.read_csv(file_path)

# rename columns
df.rename(columns=col_map, inplace=True)

# reorder to match DB table column order
df = df[list(col_map.values())]

# load into DB
df.to_sql(table, engine, if_exists='append', index=False)

print(f"Loaded into '{table}'")


"""
Python script to load indicator columns data representing geographical regions, 
sub-regions, based on geography and economic conditions

This code chunk has to be run separately from the one at the top as this table is 
not in the mapping.

"""
# load required packages
import os
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection 
engine = create_engine('postgresql+psycopg2://postgres:1995@localhost:5432/faostat_ms_dsci_project')

# path to the directory containing cleaned CSV files which are to be loaded
file_path = '/Users/gurjitsingh/Desktop/MS Data Science/MS_Project_Python/indicator_columns.csv'

df = pd.read_csv(file_path)

# rename columns
df.rename(
    columns={
        'area_code_M49': 'area_code_m49',
        'area': 'area',
        'region': 'region' ,
        'sub_region': 'sub_region',
        'european_union_country': 'european_union_country',
        'least_developed_country': 'least_developed_country',
        'land_locked_developing_country': 'land_locked_developing_country',
        'small_island_developing_state': 'small_island_developing_state',
        'low_income_food_deficit_country': 'low_income_food_deficit_country',
        'net_food_importing_developing_country': 'net_food_importing_developing_country'
    }, inplace=True)

table = "indicator_columns"
# load into DB
df.to_sql(table, engine, if_exists='append', index=False)

print(f"Loaded into '{table}'")