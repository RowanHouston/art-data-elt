import requests
import json
import os
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
extraction_path = os.path.join(raw_dir, "met_objects.ndjson")

headers = {"User-Agent": "art-etl-project/1.0 (rowanhouston2@gmail.com)"}


ids_response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects", headers = headers)
ids_list = ids_response.json()["objectIDs"] #len = ~500k

fetched_ids = set()
if os.path.exists(extraction_path):
    with open(extraction_path, "r") as f:
        for line in f:
            record = json.loads(line)
            fetched_ids.add(record["objectID"])

num_records_fetched = 0
with open(extraction_path, "a") as f:
    for object_id in ids_list:
        if object_id in fetched_ids:
            continue
        while True:
            try:
                response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}", headers=headers)
            except requests.exceptions.ConnectionError as e:
                print(f"connection error on {object_id}: {e}, retrying in 60s")
                time.sleep(60)
                continue
            #Met server occasionally dropping connection around 15k records

            
            if response.status_code == 200:
                record = response.json()
                f.write(json.dumps(record) + "\n")
                num_records_fetched +=1
                if num_records_fetched % 1000 == 0:
                    print(f"{num_records_fetched} records fetched successfully")
                    f.flush()
                time.sleep(1)
                #met server rate limiting at any lower value despite docs indicating 80/second rate threshold
                break
            elif response.status_code == 403:
                print(f"rate limited on {object_id}")
                time.sleep(60)
                #met server commonly returns 403 when rate limited instead of usual 429
            else:
                print(f"skipped {object_id}: status {response.status_code}")
                break        