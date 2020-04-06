from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_info = mongo.db.mars_info.find_one()
    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# route that will trigger the scrape
@app.route("/scrape")
def scrape():

    # Run the scrape functions
    mars_info = mongo.db.mars_info    
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)