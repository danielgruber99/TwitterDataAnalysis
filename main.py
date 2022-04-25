import os
import csv
import tweepy
import pandas
import csv



def main():
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    print(bearer_token)
    #client = tweepy.Client(bearer_token=bearer_token,
    #consumer_key = consumer_key, 
    #consumer_secret = consumer_secret,
    #access_token = access_token,
    #access_token_secret= access_token_secret,)
    client = tweepy.Client(bearer_token=bearer_token)

    tweets = client.search_recent_tweets(query="computer", max_results=10)



    print(tweets)
    #auth = tweepy.OAuth2BearerHandler('AAAAAAAAAAAAAAAAAAAAABqKbgEAAAAAS2RKvDrWSBI4OGvmZz8Qqe%2Bmg%2F0%3D20aat5g0H71Cj1yiBDTyAJSENfzO3cYZ3VWCJfnWywIC7OiIZz')

if __name__ == "__main__":
    main()

