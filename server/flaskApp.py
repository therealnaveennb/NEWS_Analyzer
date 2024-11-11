from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient, server_api
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
import ssl

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
# Function to connect to MongoDB and retrieve data from a collection
def fetch_data_from_mongodb(collection_name):
    # Get MongoDB credentials from environment variables
    mongo_username = quote_plus(os.getenv('MONGO_USERNAME'))
    db_password = quote_plus(os.getenv('MONGO_PASSWORD'))
    db_name = os.getenv('DB_NAME')

    # MongoDB connection URI with escaped username and password
    uri = f"mongodb+srv://{mongo_username}:{db_password}@news-analyzer.0ittn.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=News-analyzer"

    # Create a new client and connect to the MongoDB server
    client = MongoClient(uri, server_api=server_api.ServerApi('1'), ssl=True,
    
    tlsAllowInvalidCertificates=True)

    # Retrieve data from the collection
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
            

    return data

# Route to fetch articles without sentiment analysis
@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        # Fetch data from MongoDB
        articles = fetch_data_from_mongodb(collection_name="PolarityData")

        # Check if the data is empty
        if not articles:
            return jsonify({"error": "No articles found"}), 404

        return jsonify(articles)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
