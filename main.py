import os
import csv
import tweepy
import pandas as pd
import csv
import textblob


from src.auth import Client
from src.menu import Menu


def main():
    
    Twitterclient = Client()  
    myMenu = Menu(Twitterclient)     
    
    Twitterclient.get_tweets('computer')
    Twitterclient.store_tweets_to_csv()


    df = pd.read_csv('fetched/computer.csv')
    


    print(df.index)
    print(df.columns)
    

    

if __name__ == "__main__":
    main()

