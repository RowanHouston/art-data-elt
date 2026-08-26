import pandas as pd
import os
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
kaggle_path = os.path.join(raw_dir, "kaggle-famous-paintings")

for file in os.listdir(kaggle_path):
    df = pd.read_csv(os.path.join(kaggle_path, file))
    df.replace(excel_errors, pd.NA, inplace=True)
    df.to_sql('kaggle_' + file, engine, schema='raw', if_exists='replace', index=False)
