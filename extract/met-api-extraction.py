import requests
import json
import os
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
extraction_path = os.path.join(raw_dir, "met_objects.ndjson")

ids_response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
ids_list = ids_response.json()["objectIDs"]

fetched_ids = set()
if os.path.exists(extraction_path):
    with open(extraction_path, "r") as f:
        for line in f:
            record = json.loads(line)
            fetched_ids.add(record["objectID"])


headers = {"User-Agent": "art-etl-project/1.0 (rowanhouston2@gmail.com)"}
num_records_fetched = 0
with open(extraction_path, "a") as f:
    for object_id in ids_list:
        if object_id in fetched_ids:
            continue
        response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}", headers=headers)
        if response.status_code == 200:
            record = response.json()
            f.write(json.dumps(record) + "\n")
            num_records_fetched +=1
        else:
            print(f"skipped {object_id}: status {response.status_code}")        
        if num_records_fetched % 100 == 0:
            print(f"{num_records_fetched} records fetched successfully")
        time.sleep(0.5)
