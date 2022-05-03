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
    

if __name__ == "__main__":
    main()

