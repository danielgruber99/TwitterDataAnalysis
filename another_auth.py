#!/usr/bin/python
import tweepy
import csv #Import csv
import os

access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Open/create a file to append data to
csvFile = open('result.csv', 'a')

#Use csv writer
csvWriter = csv.writer(csvFile)

for tweet in api.search_tweets(
                           q = "google",
                           count=10):

    # Write a row to the CSV file. I use encode UTF-8
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    #print tweet.created_at, tweet.text
csvFile.close()