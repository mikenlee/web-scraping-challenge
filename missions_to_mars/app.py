from flask import Flask, render_template, redirect
import pymongo

#instantiate flask app
app = Flask(__name__)

#Connect to mongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#connect to mars DB; create if doesn't exist
db = client.mars_db

#connect to mars collection
mars_coll = db.mars


@app.route('/')
def index():
    
    mars_data = mars_coll.find_one()
     
    return(render_template('index.html', mars_data = mars_data))

@app.route('/scrape')
def scrape():

    # this is the py script with all of the scraping functions 
    import scrape_mars
    
    #gather documents to insert
    nasa_document = scrape_mars.scrape_all()

    #insert into mars collection
    # mars_coll.insert_one(data_document)

    #upsert into database (prefered to avoid duplicates) 
    mars_coll.update_one({}, {'$set': nasa_document}, upsert = True)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)