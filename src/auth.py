from http import client
import os
from typing import List
import tweepy
import csv

class Client:

    def __init__(self, csv_filepath="result.py"):
        self.access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        self.client = tweepy.Client(bearer_token=self.bearer_token)
        #self.client.raise_for_status()       # if authentication failed raise_for_status will throw an exception
        self.tweets = None
        self.csv_filepath = csv_filepath

    def get_tweets(self, querystring):
        response = self.client.search_recent_tweets(query=querystring, tweet_fields=["created_at", "lang"], expansions=["author_id"], max_results=10)
        self.tweets = response.data
    
    def store_tweets_to_csv(self, csv_file="result.csv"):
        csvFile = open(csv_file,'w')
        csvWriter = csv.writer(csvFile)

        csvWriter.writerow(["Tweet_ID", "Tweet Text", "Tweet created_at", "user_id" ])
        for tweet in self.tweets:
            # Write a row to the CSV file. I use encode UTF-8
            csvWriter.writerow([tweet.id, tweet.text, tweet.created_at, tweet.author_id])
            #print tweet.created_at, tweet.text
        csvFile.close()


