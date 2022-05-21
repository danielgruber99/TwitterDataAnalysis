from http import client
import os
from typing import List
import tweepy
import csv
import pandas as pd
import src.constants as const

class TwitterClient:

    def __init__(self):
        # authentication to Twitter Endpoint API v2
        self.client = None
        self.authenticate()
        self.tweets = None
        self.users = None
        # set default querystring to computer
        self.querystring = 'computer'
        self.csv_file_tweets = None
        self.csv_file_users = None
        self.csv_folder_path = None
        self.update_csv_file_paths()
    
    def authenticate(self):
        """
        authenticate to twitter endpoint API v2 with client
        """
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

    def fetch_tweets(self, querystring):
        self.querystring = querystring
        self.update_csv_file_paths()
        # get response for querystring and only consider tweets (no retweets) in english with at least one hashtag
        response = self.client.search_recent_tweets(query=f'{self.querystring} lang:en -is:retweet has:hashtags', tweet_fields=["created_at", "lang", "entities"], expansions=["author_id"], max_results=const.NR_TWEETS)
        # store tweets to csv
        self.create_folder(f"fetched/{self.querystring}")
        # create tweets dataframe and store it to csv file
        columns = [const.tweet_id, const.tweet_text, const.tweet_hashtags, const.tweet_createdAt, const.user_id]
        data = []
        for tweet in response.data:
            hashtags = self.extract_hashtags(tweet)
            data.append([tweet.id, tweet.text, hashtags, tweet.created_at, tweet.author_id])    
        tweets_df = pd.DataFrame(data, columns=columns)
        tweets_df.to_csv(self.csv_file_tweets)
    
    def fetch_users(self):
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

    def extract_hashtags(self, tweet) -> list:
        """
        extract hashtag von retrieved response.data dictionary

        Returns:
        --------
        hashtags_string:    string of all hashtags separated by a comma (for later splitting again)
        """
        entity_hashtag = tweet.entities["hashtags"]
        hashtags = []
        for hashtag in entity_hashtag:
            hashtags.append(hashtag['tag'])
        hashtags_string = ','.join(hashtags)
        return hashtags_string

    def fetch_followers(self, userid):
        """
        fetch followers for a given user ID.
        """
        #TODO: check if followers csv file already exists... if not do below, else just load csv file and return as dataframe
        self.create_folder(f"fetched/{self.querystring}/followers")
        response_followers = self.client.get_users_followers(userid, user_fields=['description'], max_results=500)
        followers = response_followers.data
        columns = [const.user_id, 'name', 'username', 'bio']        # description in user is better known as bio (profile of user)
        data = []
        for follower in followers:
            data.append([follower.id, follower.name, follower.username, follower.description])
        followers_df = pd.DataFrame(data, columns=columns)
        followers_df.to_csv(f"{self.csv_folder_path}followers/{userid}_followers.csv")
        return followers_df

    def fetch_tweets_of_followers(self, followerids):
        """
        fetches tweets of specified user. Especially used for fulfilling Task4.
        """
        columns = [const.follower_id, const.tweet_id, const.tweet_text]
        data = []
        for followerid in followerids:
            response = self.client.get_users_tweets(followerid, max_results=20)
            tweets_of_follower = response.data
            if tweets_of_follower is not None:
                for follower_tweet in tweets_of_follower:
                    data.append([followerid, follower_tweet.id, follower_tweet.text])
        follower_tweets_df = pd.DataFrame(data, columns=columns)
        return follower_tweets_df


    def lookup_user(self, userid):
        """
        lookup username for given user ID.
        """
        response = self.client.get_user(id=userid, user_fields=["name","username"])
        #print(response.data)
        return response.data.username



