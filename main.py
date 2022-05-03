import os
import csv
import tweepy
import pandas as pd
import csv
import textblob


from src.twitterclient_v2 import TwitterClient_v2
from src.menu import Menu


def main():
    default_querystring = "computer"

    twitterclient_v2 = TwitterClient_v2()  
    twitterclient_v2.get_tweets(default_querystring)
    twitterclient_v2.store_tweets_to_csv()
    myMenu = Menu(twitterclient_v2)        
    

if __name__ == "__main__":
    main()

