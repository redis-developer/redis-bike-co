from dotenv import load_dotenv
from flask import Flask
from redis.commands.search.aggregation import AggregateRequest
from redis.commands.search.query import Query
from redis.exceptions import ResponseError

import json
import os
import redis

# Load environment variables / secrets from .env file.
load_dotenv()

STORE_KEY_BASE = os.getenv("STORE_KEY_BASE")
BIKE_KEY_BASE = os.getenv("BIKE_KEY_BASE")
BIKE_INDEX_NAME = os.getenv("BIKE_INDEX_NAME")
STORE_INDEX_NAME = os.getenv("STORE_INDEX_NAME")

# Connect to Redis.
redis_client = redis.from_url(os.getenv("REDIS_URL"))

app = Flask(__name__)

# Find stores within a given radius of a point that have certain amenities.
# ft.search idx:stores "@position:[80.8599399 26.848668 100 km] @amenities{wifi} @amenities{cafe}"
@app.route("/api/storesnearby/<lat>/<lng>/<int:radius>/<unit>/<amenities>")
def stores_in_radius(lat, lng, radius, unit, amenities):
    all_amenities = amenities.split(",")
    amenities_clause = ""

    for amenity in all_amenities:
        amenities_clause = f"{amenities_clause} @amenities:{{{amenity}}} "
       
    result = redis_client.ft(STORE_INDEX_NAME).search(
       Query(f"@position:[{lng} {lat} {radius} {unit}] {amenities_clause}")
    )
   
    vals = []

    for doc in result.docs:
        vals.append(json.loads(doc["json"]))

    return dict(data = vals)

# Find all the different values of an indexed attribute.
# ft.aggregate idx:bikes "*" groupby 1 @<attr>
@app.route("/api/valuesfor/<attr>", methods = ["GET"])
def values_for_attr(attr):
    vals = []

    try:
        result = redis_client.ft(BIKE_INDEX_NAME).aggregate(
           AggregateRequest("*").group_by([f"@{attr}"])
        )

        for r in result.rows:
           # r = [ "attr", "val" ]
           vals.append(r[1])

    except ResponseError:
       # Attribute was not indexed.
       pass
       
    return dict(data = vals)

# Find all the bikes in a given price range that are not for kids
# and allow pagination through them.  Sort by price descending.
# ft.search idx:bikes "(-@type:{Kids Bikes|Kids Mountain Bikes}) @price:[<min> <max>]" sortby price desc return 4 stockcode brand model price limit <offset> <num_results>
@app.route("/api/adultbikes/<int:min>/<int:max>/<int:offset>/<int:num_results>", methods = ["GET"])
def find_adult_bikes_in_range(min, max, offset, num_results):
    vals = []
   
    results = redis_client.ft(BIKE_INDEX_NAME).search(
        Query(f"(-@type:{{Kids Bikes|Kids Mountain Bikes}}) @price:[{min} {max}]")
            .sort_by("price", asc = False)
            .return_fields("stockcode", "brand", "model", "price")
            .paging(offset, num_results))

    for doc in results.docs:  
        vals.append(dict(
            stockcode = doc["stockcode"],
            brand = doc["brand"],
            model = doc["model"],
            price = doc["price"]
        ))
   
    return dict(data = vals)
   
# Get all details for store having a given store code.
# json.get redisbikeco:store:<storecode> $
@app.route("/api/storedetails/<storecode>", methods = ["GET"])
def get_store_details(storecode):
   details = redis_client.json().get(f"{STORE_KEY_BASE}:{storecode}", "$")

   return dict(data = details)

# Get the brand, model and price for a bike given a stock code.
@app.route("/api/bikedetails/<stockcode>", methods = ["GET"])
def get_bike_details_for_stockcode(stockcode):
    vals = []

    details = redis_client.json().get(
      f"{BIKE_KEY_BASE}:{stockcode}", "$.brand", "$.model", "$.price"
    )

    if details:
        vals.append(dict(
            brand = details["$.brand"][0],
            model = details["$.model"][0],
            price = details["$.price"][0]
        ))

    return dict(data = vals)

@app.route("/", methods = ["GET"])
def home_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Redis Bike Company Demo</title>
        </head>
        <body>
            <h1>Redis Bike Company Demo</h1>
            <p>Example queries:</p>
            <ul>
                <li><a target="_blank" href="/api/storesnearby/26.848668/80.8599399/10000/km/wifi,rentals">Find stores near location</a>.</li>
                <li><a target="_blank" href="/api/valuesfor/brand">Find distinct values for a tag</a>.</li>
                <li><a target="_blank" href="/api/adultbikes/20000/300000/0/2">Find bikes matching multiple criteria</a>.</li>
                <li><a target="_blank" href="/api/storedetails/ch">Get all store details for a given store</a>.</li>
                <li><a target="_blank" href="/api/bikedetails/rbc00004">Get some details about a bike given a stockcode</a>.</li>
            </ul>
            <p><a href="https://github.com/redis-developer/redis-bike-co">Read the documentation on GitHub</a>.</p>
        </body>
    </html>
    """