from dotenv import load_dotenv
from flask import Flask
from redis.commands.search.aggregation import AggregateRequest
from redis.commands.search.query import Query
from redis.exceptions import ResponseError

import os
import redis

# Load environment variables / secrets from .env file.
load_dotenv()

BIKE_INDEX_NAME = "idx:bikes" # TODO move to .env and same in data loader.
STORE_INDEX_NAME = "idx:stores"
# TODO KEY NAMING CONSTANTS AND MOVE TO .env... and same in data loader.

# Connect to Redis.
redis_client = redis.from_url(os.getenv("REDIS_URL"))

app = Flask(__name__)

# TODO Find stores within a given radius of a point that have certain amenities.


# Find all the different values of an indexed attribute.
# ft.aggregate idx:bikes "*" groupby 1 @<attr>
@app.route("/api/valuesfor/<attr>", methods = ["GET"])
def values_for_attr(attr):
    vals = []

    try:
        result = redis_client.ft(BIKE_INDEX_NAME).aggregate(AggregateRequest("*").group_by([f"@{attr}"]))

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
   
    results = redis_client.ft(BIKE_INDEX_NAME).search(Query(f"(-@type:{{Kids Bikes|Kids Mountain Bikes}}) @price:[{min} {max}]").sort_by("price", asc = False).return_fields("stockcode", "brand", "model", "price").paging(offset, num_results))

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
   details = redis_client.json().get(f"redisbikeco:store:{storecode}", "$")

   return dict(data = details)

# Get the brand, model and price for a bike given a stock code.
@app.route("/api/bikedetails/<stockcode>", methods = ["GET"])
def get_bike_details_for_stockcode(stockcode):
   vals = []

   details = redis_client.json().get(f"redisbikeco:bike:{stockcode}", "$.brand", "$.model", "$.price")

   if details:
      vals.append(dict(
         brand = details["$.brand"][0],
         model = details["$.model"][0],
         price = details["$.price"][0]
      ))

   return dict(data = vals)

# TODO add links to all the routes...
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
            <p><a href="https://github.com/redis-developer/redis-bike-co">Read the documentation on GitHub</a>.</p>
        </body>
    </html>
  """