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
if os.path.exists("raw/met_objects.ndjson"):
    with open("raw/met_objects.ndjson", "r") as f:
        for line in f:
            record = json.loads(line)
            fetched_ids.add(record["objectID"])

with open("raw/met_objects.ndjson", "a") as f:
    for object_id in ids_list:
        if object_id in fetched_ids:
            continue
        response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}")
        if response.status_code == 200:
            record = response.json()
            f.write(json.dumps(record) + "\n")
        time.sleep(0.1)

