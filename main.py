import os
import csv
import tweepy
import pandas as pd
import csv
import textblob


from src.twitterclient_v2 import TwitterClient_v2
from src.menu import Menu
from src.dataprocessing import DataProcessing

def main():
    # prefetch of topic computer
    default_topic = "computer"
    twitterclient_v2 = TwitterClient_v2()  
    twitterclient_v2.get_tweets(default_topic)

    # start menu
    myMenu = Menu(twitterclient_v2)        


if __name__ == "__main__":
    main()

