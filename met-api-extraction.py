import requests
import json
import os

extract_dir = os.path.dirname(os.path.abspath(__file__))
extraction_path = os.path.join(extract_dir, "met_objects.ndjson")


fetched_ids = set()

# ids_response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
# ids_list = ids_response.json()["objectIDs"]

# object_num = 1
# url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_num}"
# r = requests.get(url)
# if r.status_code == 200:
#     print("Request was successful!")
# else:
#     print(f"Failed to retrieve data. Status code: {r.status_code}")
# response_json = r.json()
# print(response_json)

r = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")
r_json = r.json()
print(r_json)