from http import client
import os
from typing import List
import tweepy
import csv
import pandas as pd
import src.constants as const

class TwitterClient_v2:

    def __init__(self):
        self.access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        # logon to api v2 endpoint
        try:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        except:
            print("Error: Authentication Failed!")
        self.tweets = None
        self.users = None
        # set default querystring to computer
        self.querystring = 'computer'
        self.csv_file_tweets = None
        self.csv_file_users = None
        self.csv_folder_path = None
        self.update_csv_file_paths()
    
    def create_folder(self, folder):
        """
        For each querystring a dedicated folder will be created under 'fetched/'. This function will check if the folder already exists and, if not, creates it.
        """
        folder = (folder)
        CHECK_FOLDER = os.path.isdir(folder)

        if not CHECK_FOLDER:
            os.makedirs(folder)
        else:
            pass

    def update_csv_file_paths(self):
        self.csv_file_tweets = f'fetched/{self.querystring}/{self.querystring}.csv'
        self.csv_file_users = f'fetched/{self.querystring}/{self.querystring}_users.csv'
        self.csv_folder_path = f'fetched/{self.querystring}/'

    def get_tweets(self, querystring):
        self.querystring = querystring
        self.update_csv_file_paths()
        # get response for querystring and only consider tweets (no retweets) in english with at least one hashtag
        response = self.client.search_recent_tweets(query=f'{self.querystring} lang:en -is:retweet has:hashtags', tweet_fields=["created_at", "lang", "entities"], expansions=["author_id"], max_results=20)
        # write fetched data to member variable tweets
        self.tweets = response.data
        # store tweets to csv
        self.store_tweets_to_csv()
    
    def store_tweets_to_csv(self, override_csv_file=None):
        self.create_folder(f"fetched/{self.querystring}")
        if override_csv_file is None:
            csvFile = open(self.csv_file_tweets, 'w')
        else:
            csvFile = open(override_csv_file, 'w')

        csvWriter = csv.writer(csvFile)

        columns = [const.tweet_id, const.tweet_text, const.tweet_entities, const.tweet_createdAt, const.user_id, 'hashtags' ]
        data = []

        for tweet in self.tweets:
            hashtags = self.extract_hashtags(tweet)
            data.append([tweet.id, tweet.text, tweet.entities, tweet.created_at, tweet.author_id, hashtags])
        
        tweets_df = pd.DataFrame(data, columns=columns)
        tweets_df.to_csv(self.csv_file_tweets)


        #csvWriter.writerow(columns)
              
        # maybee convert it first to pandas.Dataframe and then use DataFrame.to_csv!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #for tweet in self.tweets:
            # Write a row to the CSV file. I use encode UTF-8
        #    csvWriter.writerow([tweet.id, tweet.text, tweet.entities, tweet.created_at, tweet.author_id])
            #print tweet.created_at, tweet.text
        csvFile.close()
    
    def get_users(self):
        if self.tweets is None:
            self.get_tweets(self.querystring)
        
        users_with_duplicates = self.tweets[const.user_id]
        users = list(set(users_with_duplicates))
        
        start = 0
        length_users = len(users)

        columns = []
        data = []

        #response_list = []
        #for hundred_user_list in users:
        #    if start+100 =< len(users_wo_duplicates): 
        #        response =  self.client.get_users(hundred_user_list[start:start+100])
        #        response
        #        start+=100
        #    else:
        #        response += self.client.get_users(hundred_user_list[start:length_users])
        response_list = []
        for user in users:
            self.client.get_user(user)
            




    def store_users_to_csv(self, override_csv_file=None):
        self.create_folder()
        if override_csv_file is None:
            csvFile = open(self.csv_file_users, 'w')
        else:
            csvFile = open(override_csv_file, 'w')

        csvWriter = csv.writer(csvFile)

        columns = [const.user_id]
        data = []

        for user in self.users:
            hashtags = self.extract_hashtags(tweet)
            data.append([tweet.id, tweet.text, tweet.entities, tweet.created_at, tweet.author_id, hashtags])
        
        tweets_df = pd.DataFrame(data, columns=columns)
        tweets_df.to_csv(self.csv_file_users)
        csvFile.close()

    def extract_hashtags(self, tweet) -> list:
        entity_hashtag = tweet.entities["hashtags"]
        hashtags = []
        for hashtag in entity_hashtag:
            hashtags.append(hashtag['tag'])
        hashtags_string = ','.join(hashtags)
        return hashtags_string

    def get_followers(self, userid):
        #TODO: check if followers csv file already exists... if not do below, else just load csv file and return as dataframe
        self.create_folder(f"fetched/{self.querystring}/followers")
        response_followers = self.client.get_users_followers(userid)
        followers = response_followers.data
        columns = [const.user_id, 'name', 'username']
        data = []
        for follower in followers:
            data.append([follower.id, follower.name, follower.username])
        followers_df = pd.DataFrame(data, columns=columns)
        followers_df.to_csv(f"{self.csv_folder_path}followers/{userid}_followers.csv")
        return followers_df

    def lookup_user(self, userid):
        response = self.client.get_user(id=userid)
        print(response.data)
        return 'test' #response.data.username


