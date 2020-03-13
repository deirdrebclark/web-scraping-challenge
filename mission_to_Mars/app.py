from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template('index.html', mars = mars)
 

#Use scrape_mars to get information on Mars
@app.route("/scrape")
def scraper():

    mars_data = scrape_mars.scrape()

    #Store results into a dictionary
    print(mars_data)
    mars = {
        'news_title':mars_data['news_title'],
        'news_paragraph':mars_data['news_paragraph'],
        'featured_image':mars_data['featured_image_url'],
        'weather':mars_data['mars_weather'],
        'table':mars_data['table'],
        'hemisphere_image_urls':mars_data['hemisphere_image_urls'],        
    }
   
    # Insert mars data into database
    mongo.db.collection.insert_one(mars)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
