import json
import asyncio
import aiohttp
import os


CONCURRENCY_LIMIT = 1

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
extraction_path = os.path.join(raw_dir, "met_objects.ndjson")

async def fetch_object(session, semaphore, object_id):
    async with semaphore:
        asyncio.sleep(0.5)
        for attempt in range(5):
            try:
                async with session.get(
                    f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status in (403, 429):
                        wait = 2 ** attempt
                        print(f"rate limited on {object_id}, waiting {wait}s")
                        await asyncio.sleep(wait)
                    else:
                        print(f"skipped {object_id}: status {response.status}")
                        return None
            except Exception as e:
                print(f"error on {object_id}: {e}")
                await asyncio.sleep(2 ** attempt)
        return None

async def extract_all(extraction_path):
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    fetched_ids = set() 
    async with aiohttp.ClientSession(
        headers={"User-Agent": "art-etl-project/1.0 (rowanhouston2@email.com)"}
    ) as session:
        async with session.get("https://collectionapi.metmuseum.org/public/collection/v1/objects") as response:
            data = await response.json()
            ids_list = data["objectIDs"]
        
        if os.path.exists(extraction_path):
            with open(extraction_path, "r") as f:
                for line in f:
                    record = json.loads(line)
                    fetched_ids.add(record["objectID"])
        
        ids_to_fetch = [oid for oid in ids_list if oid not in fetched_ids]
        with open(extraction_path, "a") as f:
            tasks = [fetch_object(session, semaphore, oid) for oid in ids_to_fetch]
            for coro in asyncio.as_completed(tasks):
                record = await coro
                if record:
                    f.write(json.dumps(record) + "\n")

asyncio.run(extract_all(extraction_path))