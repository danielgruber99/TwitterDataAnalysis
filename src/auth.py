import os
import tweepy

class Client:
    #client = tweepy.Client(bearer_token=bearer_token,
    #consumer_key = consumer_key, 
    #consumer_secret = consumer_secret,
    #access_token = access_token,
    #access_token_secret= access_token_secret,)

    def __init__(self):
        self.access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    
    def get_client(self):
        return tweepy.Client(bearer_token=self.bearer_token)


