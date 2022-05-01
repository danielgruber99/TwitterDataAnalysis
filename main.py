import os
import csv
import tweepy
import pandas as pd
import csv
import textblob


from src.auth import Client
from src.menu import Menu


def main():
    
    #myMenu = Menu()
    Twitterclient = Client('computer')       
    
    Twitterclient.get_tweets()
    Twitterclient.store_tweets_to_csv()


    df = pd.read_csv('computer.csv')
    df.to_csv("")

    analysis = textblob.TextBlob(df['Tweet Text'][0])
    print(analysis.sentiment)


    print(df.index)
    print(df.columns)
    

    

if __name__ == "__main__":
    main()

