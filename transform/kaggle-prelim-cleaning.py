import pandas as pd
import os

excel_errors = ['#VALUE!', '#N/A', '#REF!', '#DIV/0!', '#NAME?', '#NULL!', '#NUM!']

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
kaggle_path = os.path.join(raw_dir, "kaggle-famous-paintings")

for file in os.listdir(kaggle_path):
    df = pd.read_csv(os.path.join(kaggle_path, file))
    df.replace(excel_errors, pd.NA, inplace=True)
    df.to_csv(os.path.join(project_root, "cleaned", "famous-paintings-cleaned", file + "-cleaned.csv"), index=False)