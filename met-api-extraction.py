import requests
import json

object_num = 1
url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_num}"
r = requests.get(url)
if r.status_code == 200:
    print("Request was successful!")
else:
    print(f"Failed to retrieve data. Status code: {r.status_code}")
response_json = r.json()
print(response_json)