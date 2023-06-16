from flask import Flask

app = Flask(__name__)

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