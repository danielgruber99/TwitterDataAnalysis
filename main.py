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
    #client = tweepy.Client(bearer_token=bearer_token,
    #consumer_key = consumer_key, 
    #consumer_secret = consumer_secret,
    #access_token = access_token,
    #access_token_secret= access_token_secret,)
    client = tweepy.Client(bearer_token=bearer_token)

    response = client.search_recent_tweets(query="computer", tweet_fields=["created_at", "lang"], expansions=["author_id"], max_results=10)
    tweets = response.data
   
    csvFile = open('result.csv','w')
    csvWriter = csv.writer(csvFile)

    csvWriter.writerow(["Tweet ID", "Tweet Text", "Tweet created_at", "user_id" ])
    for tweet in tweets:

        # Write a row to the CSV file. I use encode UTF-8
        csvWriter.writerow([tweet.id, tweet.text, tweet.created_at, tweet.author_id])
        #print tweet.created_at, tweet.text
    csvFile.close()
            


    print(tweets)
    

if __name__ == "__main__":
    main()

