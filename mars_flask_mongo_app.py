#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 21:01:38 2018

@author: SKB
"""
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    print("Inside INDEX.HTML")
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)
    #return render_template("index2.html", mars=mars)

@app.route("/scrape")
def scrape():
    print("Inside scrape")
    mars = mongo.db.mars
    mars_data = mars_scrape.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return "Scraping Successful!"


if __name__ == "__main__":
    app.run(debug=True)