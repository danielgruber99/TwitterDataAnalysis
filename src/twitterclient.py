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
            self.client = None
            print("Error: Authentication Failed!")
    
    def fetch_tweets(self, querystring):
        """
        fetch tweets for given querystring. Only tweets in language english, with at least one hashtag are searched. Retweets are excluded.
        """
        # get response for querystring and only consider tweets (no retweets) in english with at least one hashtag
        tweets_df = None
        if self.client:
            try:
                response = self.client.search_recent_tweets(query=f'{self.querystring} lang:en -is:retweet has:hashtags', tweet_fields=["created_at", "lang", "entities"], expansions=["author_id"], max_results=const.NR_TWEETS)
                columns = [const.tweet_id, const.tweet_text, const.tweet_hashtags, const.tweet_createdAt, const.user_id]
                data = []
                for tweet in response.data:
                    hashtags = self.extract_hashtags(tweet)
                    data.append([tweet.id, tweet.text, hashtags, tweet.created_at, tweet.author_id]) 
                    tweets_df = pd.DataFrame(data, columns=columns)
            except tweepy.errors.Unauthorized as unauthorized:
                print("Unauthorized:", unauthorized)
                print("Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
            except tweepy.errors.TooManyRequests as toomanyrequests:
                print("TooManyRequests:", toomanyrequests)
                print("You have done too many requests. Try again in approximately 15 minutes.")
        else:
            print("The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
        return tweets_df
    
    def fetch_users(self, userids):
        """
        fetch IDs, names and usernames of given userids in previously fetched set of tweets.
        Required for providing the user the possibility to browse through all users.
        """
        columns = [const.user_id, const.user_name, const.user_username]
        data = []
        if self.client:
            for userid in userids:
                try:
                    response = self.client.get_user(id=userid, user_fields=['id','name','username'])
                    user = response.data
                    # handle if for user no data could be fetched but also no error was trown by the Twitter API
                    if user:
                        data.append([user.id, user.name, user.username])
                except tweepy.errors.Unauthorized as unauthorized:
                    print("Unauthorized:", unauthorized)
                    print("Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
                    return None
                except tweepy.errors.TooManyRequests as toomanyrequests:
                    print("TooManyRequests:", toomanyrequests)
                    print("You have done too many requests. Try again in approximately 15 minutes.")
                    return None
        else:
            print("The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
            return None
        users_df = pd.DataFrame(data, columns=columns)
        return users_df

    def extract_hashtags(self, tweet) -> list:
        """
        extract hashtags von retrieved response.data dictionary

        Returns:
        --------
        hashtags_string:    string of all hashtags separated by commas (for later splitting again)
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
        followers_df = None
        if self.client:
            try:
                response_followers = self.client.get_users_followers(userid, user_fields=['created_at','description','entities','id','location','name','profile_image_url', 'public_metrics'], max_results=const.NR_FOLLOWERS)
            except tweepy.errors.Unauthorized as unauthorized:
                print("Unauthorized:", unauthorized)
                print("Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
            except tweepy.errors.TooManyRequests as toomanyrequests:
                print("TooManyRequests:", toomanyrequests)
                print("You have done too many requests. Try again in approximately 15 minutes.")
            else:
                followers = response_followers.data
                columns = [const.follower_id, const.follower_name, const.follower_username, const.follower_bio, const.follower_bio, const.follower_created_at, const.follower_public_metrics, const.follower_profile_image_url]        # description in user is better known as bio (profile of user)
                data = []
                if followers:
                    for follower in followers:
                        data.append([follower.id, follower.name, follower.username, follower.description, follower.location, follower.created_at, follower.public_metrics, follower.profile_image_url])
                    followers_df = pd.DataFrame(data, columns=columns)
        else:
            print("The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
        return followers_df

    def fetch_tweets_of_followers(self, followerids):
        """
        fetches tweets of specified user. Especially used for fulfilling Task4.
        """
        columns = [const.follower_id, const.tweet_id, const.tweet_text]
        data = []
        if self.client:
            for followerid in followerids:
                try:
                    response = self.client.get_users_tweets(followerid, max_results=20)
                except tweepy.errors.Unauthorized as unauthorized:
                    print("Unauthorized:", unauthorized)
                    print("Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
                    return None
                except tweepy.errors.TooManyRequests as toomanyrequests:
                    print("TooManyRequests:", toomanyrequests)
                    print("You have done too many requests. Try again in approximately 15 minutes.")
                    return None
                else:
                    tweets_of_followers = response.data
                    if tweets_of_followers is not None:
                        for follower_tweet in tweets_of_followers:
                            data.append([followerid, follower_tweet.id, follower_tweet.text])
        else:
            print("The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
        followers_tweets_df = pd.DataFrame(data, columns=columns)
        return followers_tweets_df

    def lookup_user(self, userid):
        """
        lookup username for given user ID.
        """
        if self.client:
            try:
                response = self.client.get_user(id=userid, user_fields=["name","username"])
            except tweepy.errors.Unauthorized as unauthorized:
                print("Unauthorized:", unauthorized)
                print("Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets.")
            except tweepy.errors.TooManyRequests as toomanyrequests:
                print("TooManyRequests:", toomanyrequests)
                print("You have done too many requests. Try again in approximately 15 minutes.")
            else:
                user = response.data
                if user:
                    return user.username
        else:
            return None
