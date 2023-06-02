# Redis Bike Company Demo Application: Data Loader Script

from dotenv import load_dotenv

import argparse
import json
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
    # TODO drop any other indices...
except:
    # Dropping an index that doesn't exist throws an exception 
    # but isn't an error in this case.
    pass

print("TODO Create search index for bikes.")
print("TODO Create search index for stores.")

print(f"TODO Loading bike data.")
bikes_loaded = 0
# TODO open the JSON file and load the bikes...

print(f"TODO Loaded {bikes_loaded} bikes into Redis.")

print(f"TODO Loading store data.")
stores_loaded = 0
# TODO open the JSON file and load the stores...

print(f"TODO Loaded {stores_loaded} stores into Redis.")

print("Verifying data...")

try:
    print("TODO verify something")
except AssertionError as e:
    # Something went wrong :(
    print("Data verification checks failed:")
    print(e)
    redis_client.quit()
    os._exit(1)

# All done!    
print("Data verification checks completed OK.")
redis_client.quit()