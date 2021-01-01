from flask import Flask, render_template
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

#instantiate flask app
app = Flask(__name__)


#Connect to mongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)



@app.route('/')
def index():
    #code here

@app.route('/scrape')
def scrape():
    
    #connect to mars DB; create if doesn't exist
    db = client.mars_db

#connect to mars collection
mars = db.mars
#gather documents to insert
data_document = scrape_all()

#insert into mars collection
# mars.insert_one(data_document)

#upsert into database (prefered to avoid duplicates) 
mars.update_one({}, {'$set': data_document}, upsert = True)

if __name__ == '__main__':
    app.run(debug=True)