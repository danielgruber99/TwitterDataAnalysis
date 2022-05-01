from http import client
import os
from typing import List
import tweepy
import csv

class Client:

    def __init__(self, querystring):
        self.access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        self.client = tweepy.Client(bearer_token=self.bearer_token)
        #self.client.raise_for_status()       # if authentication failed raise_for_status will throw an exception
        self.tweets = None
        self.querystring = querystring
        self.csv_file = f'{querystring}.csv'

    def get_tweets(self):
        response = self.client.search_recent_tweets(query=f'{self.querystring} lang:en -is:retweet has:hashtags', tweet_fields=["created_at", "lang", "entities"], expansions=["author_id"], max_results=10)
        self.tweets = response.data
    
    # add possiblity to override store csvfilepath
    def store_tweets_to_csv(self):#csv_vile):
        csvFile = open(self.csv_file,'w')
        csvWriter = csv.writer(csvFile)

        columns = ["Tweet_ID", "Tweet Text", "Tweet Entities" "Tweet created_at", "user_id" ]
        csvWriter.writerow(columns)
        # maybee convert it first to pandas.Dataframe and then use DataFrame.to_csv!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for tweet in self.tweets:
            # Write a row to the CSV file. I use encode UTF-8
            csvWriter.writerow([tweet.id, tweet.text, tweet.entities, tweet.created_at, tweet.author_id])
            #print tweet.created_at, tweet.text
        csvFile.close()


