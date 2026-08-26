import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import json
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

records = []
with open(os.path.join('raw', 'met_objects.ndjson')) as f:
    for line in f:
        records.append(json.loads(line))

pd.DataFrame(records).to_sql('met_objects', engine, schema='raw', if_exists='replace', index=False)