from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Scrape_Mars

app = Flask(__name__)

# Create Connection Variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars=mars_dict)

@app.route("/scrape")
def scrape():
    mars_data = Scrape_Mars.scrape()
    mongo.db_mars_dict.update({}, mars_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)