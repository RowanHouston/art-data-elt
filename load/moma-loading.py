import pandas as pd
import os
import csv
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

#This script should be run only once since there is no logic for already existing files
#Mainly just exists so that I can import the csvs into dbeaver easily for viewing as a postgres database

excel_errors = ['#VALUE!', '#N/A', '#REF!', '#DIV/0!', '#NAME?', '#NULL!', '#NUM!']
dimensions = ['Circumference (cm)', 'Depth (cm)', 'Diameter (cm)', 'Height (cm)', 'Length (cm)', 'Weight (kg)', 'Width (cm)', 'Seat Height (cm)', 'Duration (sec.)']

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
moma_path = os.path.join(raw_dir, "moma-collection")

for file in os.listdir(moma_path):
    df = pd.read_csv(os.path.join(moma_path, file), 
                 engine='python',
                 on_bad_lines='skip',
                 quoting=csv.QUOTE_ALL)

    df.replace(excel_errors, pd.NA, inplace=True)

    for col in ['BeginDate', 'EndDate']:
        df[col] = df[col].astype(str).str.replace(r'[^\d-]', '', regex=True)
        df[col] = df[col].str.strip()
        df[col] = df[col].replace({'nan': pd.NA, '': pd.NA, '-': pd.NA})
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].replace([float('inf'), float('-inf')], pd.NA)
        df[col] = df[col].where((df[col] >= -5000) & (df[col] <= 2100), other=pd.NA)
        df[col] = df[col].astype('Int64')

    df = df.drop(columns=['Dimensions'], errors='ignore')

    df.to_sql('moma_' + (file.lower())[:-4], engine, schema='raw', if_exists='replace', index=False)

