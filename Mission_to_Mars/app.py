from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars

# Flask Creation
app = Flask (__name__)

# Use PyMongo to establish connection to Mongo
app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app")
mongo = PyMongo(app)

@app.route("/")
def index(): 
    mars_hemisphere_image_url