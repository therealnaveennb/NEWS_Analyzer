import pandas as pd
import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from pymongo import MongoClient, server_api
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Download the Vader lexicon
nltk.download('vader_lexicon')
load_dotenv()

# Function to connect to MongoDB and retrieve data from a collection
def fetch_data_from_mongodb(collection_name):
    mongo_username = quote_plus(os.getenv('MONGO_USERNAME'))
    db_password = quote_plus(os.getenv('MONGO_PASSWORD'))
    db_name = os.getenv('DB_NAME')

    uri = f"mongodb+srv://{mongo_username}:{db_password}@news-analyzer.0ittn.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=News-analyzer"
    client = MongoClient(uri, server_api=server_api.ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return
    
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find({}))
    return pd.DataFrame(data)

# Function to calculate sentiment polarity using NLTK's SentimentIntensityAnalyzer
def calculate_polarity(df):
    sia = SIA()
    results = []
    
    for _, row in df.iterrows():
        # Calculate sentiment polarity
        pol_score = sia.polarity_scores(row['lems'])
        pol_score['headline'] = row['lems']
        
        # Add original fields to the results
        pol_score['title'] = row.get('title')
        pol_score['author'] = row.get('author')
        pol_score['source'] = row.get('source')
        pol_score['description']=row.get('description')
        pol_score['pub_date'] = row.get('pub_date')
        
        results.append(pol_score)
    
    # Convert results into a DataFrame
    polarity_df = pd.DataFrame.from_records(results)
    
    # Classify as positive (1), negative (-1), or neutral (0) based on compound score
    polarity_df['label'] = 0
    polarity_df.loc[polarity_df['compound'] > 0.2, 'label'] = 1
    polarity_df.loc[polarity_df['compound'] < -0.2, 'label'] = -1
    
    # Add word count to the DataFrame
    polarity_df['word_count'] = polarity_df['headline'].apply(lambda x: len(str(x).split()))
    
    return polarity_df

# Function to save polarity data to MongoDB
def save_polarity_to_mongo(polarity_df, collection_name="PolarityData"):
    mongo_username = quote_plus(os.getenv('MONGO_USERNAME'))
    db_password = quote_plus(os.getenv('MONGO_PASSWORD'))
    db_name = os.getenv('DB_NAME')

    uri = f"mongodb+srv://{mongo_username}:{db_password}@news-analyzer.0ittn.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=News-analyzer"
    client = MongoClient(uri, server_api=server_api.ServerApi('1'))

    db = client[db_name]
    collection = db[collection_name]

    # Convert DataFrame to a dictionary and insert into MongoDB
    polarity_data = polarity_df.to_dict(orient="records")
    try:
        collection.insert_many(polarity_data)
        print("Polarity data successfully saved to MongoDB.")
    except Exception as e:
        print(f"Error saving polarity data to MongoDB: {e}")

# Main function
def main():
    # Fetch data from MongoDB
    news_articles_df = fetch_data_from_mongodb(collection_name="DailyNews")
    print(news_articles_df)

    # Calculate polarity scores and include additional fields
    headlines_polarity = calculate_polarity(news_articles_df)
    
    # Save polarity data to MongoDB
    save_polarity_to_mongo(headlines_polarity)

if __name__ == "__main__":
    main()
