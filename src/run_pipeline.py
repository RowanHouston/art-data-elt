# src/run_pipeline.py
import os
import sys
import argparse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.abspath(__file__))

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

STAGES = {
    'setup': [
        'setup/create_schemas.sql',
        'setup/extensions.sql',
    ],
    'staging': [
        'staging/stg_kaggle.sql',
        'staging/stg_met.sql',
        'staging/stg_moma.sql',
        'staging/stg_ulan.sql',
    ],
    'intermediate': [
        'intermediate/resolution/kaggle_ulan_crosswalk.sql',
        'intermediate/resolution/int_met_measurements.sql',
        'intermediate/artists_unioned.sql',
        'intermediate/artworks_unioned.sql',
    ],
    'final': [
        'final/final_artists.sql',
        'final/final_artworks.sql',
    ],
}

def run_sql_file(filepath):
    with open(filepath, 'r') as f:
        sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print(f"{filepath} run successfully")

def run_stage(stage_name):
    files = STAGES.get(stage_name)
    if files is None:
        print(f"Unknown stage: {stage_name}")
        sys.exit(1)
    print(f"\nRunning stage: {stage_name}")
    for filepath in files:
        try:
            run_sql_file(os.path.join(project_root, "sql", filepath))
        except Exception as e:
            print(f"{filepath}: {e}")
            sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the art pipeline')
    parser.add_argument(
        'stages',
        nargs='*',
        help=f"Stages to run: {list(STAGES.keys())}. Runs all if omitted."
    )
    args = parser.parse_args()

    stages_to_run = args.stages if args.stages else list(STAGES.keys())

    for stage in stages_to_run:
        run_stage(stage)

    print("\nPipeline complete.")