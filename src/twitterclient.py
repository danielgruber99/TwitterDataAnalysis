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
    
    def fetch_tweets(self, querystring):
        """
        fetch tweets for given querystring. Only tweets in language english, with at least one hashtag are searched. Retweets are excluded.
        """
        self.querystring = querystring
        # get response for querystring and only consider tweets (no retweets) in english with at least one hashtag
        response = self.client.search_recent_tweets(query=f'{self.querystring} lang:en -is:retweet has:hashtags', tweet_fields=["created_at", "lang", "entities"], expansions=["author_id"], max_results=const.NR_TWEETS)
        # create tweets dataframe and store it to csv file
        columns = [const.tweet_id, const.tweet_text, const.tweet_hashtags, const.tweet_createdAt, const.user_id]
        data = []
        for tweet in response.data:
            hashtags = self.extract_hashtags(tweet)
            data.append([tweet.id, tweet.text, hashtags, tweet.created_at, tweet.author_id])    
        tweets_df = pd.DataFrame(data, columns=columns)
        return tweets_df
    
    def fetch_users(self, users):
        """
        fetch username and name of given userids in previously fetched set of tweets.
        For providing the user the possibility to browse through users.
        """
        #users_with_duplicates = self.tweets[const.user_id]
        #users = list(set(users_with_duplicates))
        columns = [const.user_id, const.user_name, const.user_username]
        data = []
        for user in users:
            response = self.client.get_user(id=user, user_fields=['id','name','username'])
            userdata = response.data
            if userdata is not None:
                data.append([userdata.id, userdata.name, userdata.username])
        users_df = pd.DataFrame(data, columns=columns)
        return users_df

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
        response_followers = self.client.get_users_followers(userid, user_fields=['created_at','description','entities','id','location','name','profile_image_url', 'public_metrics'], max_results=500)
        followers = response_followers.data
        columns = [const.follower_id, const.follower_name, const.follower_username, const.follower_bio, const.follower_bio, const.follower_created_at, const.follower_public_metrics, const.follower_profile_image_url]        # description in user is better known as bio (profile of user)
        data = []
        for follower in followers:
            data.append([follower.id, follower.name, follower.username, follower.description, follower.location, follower.created_at, follower.public_metrics, follower.profile_image_url])
        followers_df = pd.DataFrame(data, columns=columns)
        return followers_df

    def fetch_tweets_of_followers(self, followerids):
        """
        fetches tweets of specified user. Especially used for fulfilling Task4.
        """
        columns = [const.follower_id, const.tweet_id, const.tweet_text]
        data = []
        for followerid in followerids:
            response = self.client.get_users_tweets(followerid, max_results=20)
            tweets_of_followers = response.data
            if tweets_of_followers is not None:
                for follower_tweet in tweets_of_followers:
                    data.append([followerid, follower_tweet.id, follower_tweet.text])
        followers_tweets_df = pd.DataFrame(data, columns=columns)
        return followers_tweets_df

    def lookup_user(self, userid):
        """
        lookup username for given user ID.
        """
        response = self.client.get_user(id=userid, user_fields=["name","username"])
        if response.data is not None:
            return response.data.username
        else:
            return 'anonym'