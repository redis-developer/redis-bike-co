# Redis Bike Company Demo Application: Data Loader Script

from dotenv import load_dotenv

import argparse
import json
import io
import os
import redis

# Load environment variables / secrets from .env file.
load_dotenv()

BIKES_DATASET_SIZE = 0 # Number of bikes we expect to load.
STORES_DATASET_SIZE = 0 # Number of stores we expect to load.
REDIS_KEY_BASE = "redisbikeco"
BIKE_KEY_BASE = f"{REDIS_KEY_BASE}:bike"
STORE_KEY_BASE = f"{REDIS_KEY_BASE}:store"
BIKE_INDEX_NAME = "idx:bikes"
STORE_INDEX_NAME = "idx:stores"
EXIT_CODE_ERROR = 1

# TODO set up arg_parser to get the data file(s).

# Connect to Redis and reset to a known state.
print(f"Connecting to Redis.")
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/?decode_responses=True"))

print(f"Deleting any existing data with {REDIS_KEY_BASE} prefix.")
pipeline = redis_client.pipeline(transaction = False)
for k in redis_client.scan_iter(match = f"{REDIS_KEY_BASE}:*"):
    pipeline.delete(k)

pipeline.execute()

print("Dropping any existing search indices.")

try:
    redis_client.ft(BIKE_INDEX_NAME).dropindex(delete_documents = False)
    redis_client.ft(STORE_INDEX_NAME).dropindex(delete_documents = False)
except:
    # Dropping an index that doesn't exist throws an exception 
    # but isn't an error in this case - we just want to start
    # from a known point.
    pass

print("TODO Create search index for bikes.")
print("TODO Create search index for stores.")

print(f"Loading bike data.")
bikes_loaded = 0

try:
    bikes_file = io.open("data/bike_data.json")
    all_bikes = json.load(bikes_file)
    bikes_file.close()

    # Use a pipeline to load all the bike documents into Redis.
    pipeline = redis_client.pipeline(transaction = False)

    for bike in all_bikes["data"]:
        bike_key = f"{BIKE_KEY_BASE}:{bike['stockcode'].lower()}"
        pipeline.json().set(bike_key, "$", bike)
        bikes_loaded += 1
        print(f"{bike_key} - {bike['brand']} {bike['model']}")

    pipeline.execute()
except Exception as e:
    print("Failed to load bikes file:")
    print(e)
    os._exit(EXIT_CODE_ERROR)

print(f"Loaded {bikes_loaded} bikes into Redis.")

print(f"Loading store data.")
stores_loaded = 0

try:
    stores_file = io.open("data/store_data.json")
    all_stores = json.load(stores_file)
    bikes_file.close()

    # Use a pipeline to load all the store documents into Redis.
    pipeline = redis_client.pipeline(transaction = False)

    for store in all_stores["data"]:
        store_key = f"{STORE_KEY_BASE}:{store['storecode'].lower()}"
        pipeline.json().set(store_key, "$", store)
        stores_loaded += 1
        print(f"{store_key} - {store['storename']}")

    pipeline.execute()
except Exception as e:
    print("Failed to load stores file:")
    print(e)
    os._exit(EXIT_CODE_ERROR)

print(f"Loaded {stores_loaded} stores into Redis.")

print("Verifying data...")

try:
    print("TODO verify some things...")
except AssertionError as e:
    # Something went wrong :(
    print("Data verification checks failed:")
    print(e)
    redis_client.quit()
    os._exit(EXIT_CODE_ERROR)

# All done!    
print("Data verification checks completed OK.")
redis_client.quit()