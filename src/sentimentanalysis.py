import textblob
import pandas as pd
import re
import wordcloud
import numpy as np
from PIL import Image
import os

import src.constants as const
import matplotlib.pyplot as plt

class SentimentAnalysis:
    """
    This class is responsible for the Sentiment Analysis part with textblob. It will take the existing
    csv (or dataframe, tbd), analyse each tweet and write polarity and subjectivity back.
    """
    def __init__(self, querystring):
        self.querystring = querystring
        self.csv_file = f'fetched/{self.querystring}/{self.querystring}.csv'
        self.tweets = self.read_csv_file()
        self.tweets_analyzed = False
        self.avg_sentiment = None
    
    def read_csv_file(self):
        return pd.read_csv(self.csv_file, lineterminator='\n')

    def clean_tweet(self, tweet):
        """
        Utility function to clean tweet text by removing links, special characters using regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyse_all_tweets(self):
        tweets_text = self.tweets[const.tweet_text]

        analysis_list = []
        for eachtweet in tweets_text:
            cleaned_tweet = self.clean_tweet(eachtweet)
            analysis = textblob.TextBlob(cleaned_tweet)
            analysis_list.append(analysis.sentiment.polarity)
        

        self.tweets['sentiment'] = analysis_list
        self.tweets.to_csv(self.csv_file)
        #self.print_polarity_per_tweet()
        self.get_avg_polarity()
        self.tweets_analyzed = True

    def analyse_single_tweet(self, index):
        """
        analyse Polarity of single tweet.
        """
        tweet_text = self.tweets[const.tweet_text][index]
        cleaned_tweet_text = self.clean_tweet(tweet_text)
        analysis = textblob.TextBlob(cleaned_tweet_text)
        return self.get_polarity_meaning(analysis.sentiment.polarity)

    def print_polarity_per_tweet(self, startindex=0, endindex=10):
        """
        deprecated function
        """
        # check if endindex exceeds fetchet tweets
        tweets_text = self.tweets[const.tweet_text]
        tweets_polarity = self.tweets['sentiment']
        for i in range(10):
            print( self.get_polarity_meaning(tweets_polarity[i]))

    def get_avg_polarity(self):
        """
        After analysing all tweets and writing a polarity row to the dataframe (and to the csv) calculate the avg_polarity and get its textual output
        """
        avg_polarity = self.tweets['sentiment'].mean()
        avg_polarity_meaning = self.get_polarity_meaning(avg_polarity)
        self.get_avg_polarity = avg_polarity_meaning  # or should i put avg_polarity as number from -1 to 1 in here and change output in menu
        print("The average polarity of your topic '", self.querystring, "' is ", f"'{avg_polarity_meaning}'")

        

    def get_polarity_meaning(self, polarity)->str:
        """
        Translate polarity values from -1 to 1 in textual output.
        """
        if polarity > 0.8:
            return 'extremely positive'
        elif polarity > 0.3:
            return 'positive'
        elif polarity > 0.05 and polarity <= 0.3:
            return 'slightly positive'
        elif (polarity <= 0.05 or polarity >= -0.05):
            return 'neutral'
        elif polarity < -0.05 and polarity <= -0.03:
            return 'slightly negative'
        elif polarity < -0.3 and polarity <=-0.8:
            return 'negative'
        elif polarity < -0.8:
            return 'extremely negative'
        else:
            return "error!"

    def get_most_used_words(self):
        """
        Get the most used words of all tweets and make a wordcloud with the mask of the official twitterlogo.
        """
        # combine all tweets text to one string
        tweets_text = self.tweets[const.tweet_text]
        all_tweets_text = self.clean_tweet(' '.join(tweets_text))
        # get current working directory
        d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        # take official twitter logo as mask
        twitter_mask = np.array(Image.open(os.path.join(d, "wordcloud/masks/twitterlogo.png")))
        # generate wordcloud
        wc = wordcloud.WordCloud(background_color="white", max_words=30, mask=twitter_mask, contour_width=3).generate(all_tweets_text)
        # store to file
        wc.to_file(os.path.join(d, "wordcloud/generated/twitterlogo_wc.png"))
        # show
        img = Image.open("wordcloud/generated/twitterlogo_wc.png")
        img.show()










        




    