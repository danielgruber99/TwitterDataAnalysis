import os
import csv
import tweepy
import pandas as pd
import csv
import textblob


from src.auth import Client
from src.menu import Menu


def main():
    
    myMenu = Menu()
    Twitterclient = Client()       
    
    Twitterclient.get_tweets('computer')
    Twitterclient.store_tweets_to_csv()


    df = pd.read_csv('computer.csv')
    

    analysis = textblob.TextBlob(df['Tweet Text'][0])
    print(analysis.sentiment)


    print(df.index)
    print(df.columns)
    

    

if __name__ == "__main__":
    main()

