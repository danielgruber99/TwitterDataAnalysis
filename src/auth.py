from http import client
import os
from typing import List
import tweepy
import csv
import pandas as pd

class Client:

    def __init__(self):
        self.access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        try:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        except:
            print("Error: Authentication Failed!")
        self.tweets = None
        self.querystring = None
        self.csv_file = f'newfile.csv'
    
    def create_folder(self):
        """
        For each querystring a dedicated folder will be created under 'fetched/'. This function will check if the folder already exists and, if not, creates it.
        """
        folder = (f"fetched/{self.querystring}")
        CHECK_FOLDER = os.path.isdir(folder)

        if not CHECK_FOLDER:
            os.makedirs(folder)
        else:
            pass


    def get_tweets(self, querystring):
        # set querystring
        self.querystring = querystring
        # set csv_file path depending on querystring
        self.csv_file = f'fetched/{self.querystring}/{self.querystring}.csv'
        # get response for querystring and only consider tweets (no retweets) in english with at least one hashtag
        response = self.client.search_recent_tweets(query=f'{self.querystring} lang:en -is:retweet has:hashtags', tweet_fields=["created_at", "lang", "entities"], expansions=["author_id"], max_results=10)
        # write fetched data to member variable tweets
        self.tweets = response.data
    
    def store_tweets_to_csv(self, override_csv_file=None):
        self.create_folder()
        if override_csv_file is None:
            csvFile = open(self.csv_file, 'w')
        else:
            csvFile = open(override_csv_file, 'w')

        csvWriter = csv.writer(csvFile)

        columns = ["Tweet_ID", "Tweet Text", "Tweet Entities", "Tweet created_at", "user_id" ]
        data = []

        for tweet in self.tweets:
            data.append([tweet.id, tweet.text, tweet.entities, tweet.created_at, tweet.author_id])
        
        tweets_df = pd.DataFrame(data, columns=columns)
        tweets_df.to_csv(self.csv_file)


        #csvWriter.writerow(columns)
              
        # maybee convert it first to pandas.Dataframe and then use DataFrame.to_csv!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #for tweet in self.tweets:
            # Write a row to the CSV file. I use encode UTF-8
        #    csvWriter.writerow([tweet.id, tweet.text, tweet.entities, tweet.created_at, tweet.author_id])
            #print tweet.created_at, tweet.text
        csvFile.close()


