#https://courses.bootcampspot.com/courses/676/pages/10-dot-5-1-use-flask-to-create-a-web-app?module_item_id=190945

#import dependencies

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# define flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the homepage route - what to display on the homepage
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# define the scrape route - this will be our button to refresh our data
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   #.update(query_parameter, data, options)
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

#run flask
if __name__ == "__main__":
   app.run()

