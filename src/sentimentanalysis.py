import textblob
import pandas as pd
import re
import wordcloud
import numpy as np
from PIL import Image
import os

class SentimentAnalysis:
    """
    This class is responsible for the Sentiment Analysis part with textblob. It will take the existing
    csv (or dataframe, tbd), analyse each tweet and write polarity and subjectivity back.
    """
    def __init__(self, csv_file):
        # or maybe I should use 
        self.csv_file = csv_file
        self.tweets = None

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyse_all_tweets(self):
        self.tweets = pd.read_csv(f'fetched/{self.csv_file}.csv')
        tweets_text = self.tweets["Tweet Text"]

        analysis_list = []
        for eachtweet in tweets_text:
            cleaned_tweet = self.clean_tweet(eachtweet)
            analysis = textblob.TextBlob(eachtweet)
            analysis_list.append(analysis.sentiment.polarity)
        

        self.tweets['sentiment'] = analysis_list
        self.tweets.to_csv("test.csv")
        self.print_polarity_per_tweet()
        print("avg polarity: ", self.print_avg_polarity())

        self.most_used_words()
    
    def print_polarity_per_tweet(self, startindex=0, endindex=10):
        # check if endindex exceeds fetchet tweets
        tweets_text = self.tweets['Tweet Text']
        tweets_polarity = self.tweets['sentiment']
        for i in range(10):
            print( self.get_polarity_meaning(tweets_polarity[i]))

    def print_avg_polarity(self) -> str:
        return self.tweets['sentiment'].mean()

    def get_polarity_meaning(self, polarity):
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

    def most_used_words(self):
        tweets_text = self.tweets['Tweet Text']
        all_tweets_text = ' '.join(tweets_text)


        d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        twitter_mask = np.array(Image.open(os.path.join(d, "wordcloud/masks/twitterlogo.png")))

        wc = wordcloud.WordCloud(background_color="white", max_words=30, mask=twitter_mask, contour_width=3)
        wc.generate(all_tweets_text)
        wc.to_file(os.path.join(d, "twitterlogo_wc.png"))








        




    