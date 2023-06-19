from flask import Flask

app = Flask(__name__)

# TODO Get details for store having a given store code

# TODO Get just the store name for a given store code

# TODO Find stores within range of a given point

# TODO Find stores with given amenities

# TODO Find all the different types of bike that we have. 
# ft.aggregate idx:bikes "*" groupby 1 @type

# TODO Find all the different bikes we have and paginate through them.
# ft.search idx:bikes "*" return 2 brand model limit 0 10

# TODO Find bikes of a given type made of a given material in a given price range


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