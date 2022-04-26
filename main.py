import os
import csv
import tweepy
import pandas as pd
import csv

from src.auth import Client

def main():
    
    client = Client().get_client()
    response = client.search_recent_tweets(query="computer", tweet_fields=["created_at", "lang"], expansions=["author_id"], max_results=10)
    tweets = response.data
   
    csvFile = open('result.csv','w')
    csvWriter = csv.writer(csvFile)

    csvWriter.writerow(["Tweet ID", "Tweet Text", "Tweet created_at", "user_id" ])
    for tweet in tweets:

        # Write a row to the CSV file. I use encode UTF-8
        csvWriter.writerow([tweet.id, tweet.text, tweet.created_at, tweet.author_id])
        #print tweet.created_at, tweet.text
    csvFile.close()
            
    

    df = pd.read_csv('result.csv')
    print(df.index)
    print(df.columns)
    

if __name__ == "__main__":
    main()

