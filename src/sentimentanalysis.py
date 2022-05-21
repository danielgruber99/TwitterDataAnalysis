import textblob
import pandas as pd
import numpy as np
import re
import wordcloud
import numpy as np
from PIL import Image
import os

import src.constants as const
import matplotlib
import matplotlib.pyplot as plt

class SentimentAnalysis:
    """
    This class is responsible for the Sentiment Analysis part with textblob. It will take the existing
    csv (or dataframe, tbd), analyse each tweet and write polarity and subjectivity back.
    """
    def __init__(self, tweets):
        # list of tweets_text
        self.tweets = tweets
        # boolean to decide whether to analyse or not
        self.tweets_analyzed = False
        # store avg_sentiment
        self.avg_sentiment = None

    def clean_tweet(self, tweet):
        """
        Utility function to clean tweet text by removing links, special characters using regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyse_all_tweets(self):
        """
        analysing all tweets and get average polarity as output.
        """
        polarity_list = []
        for eachtweet in self.tweets:
            cleaned_tweet = self.clean_tweet(eachtweet)
            analysis = textblob.TextBlob(cleaned_tweet)
            polarity_list.append(analysis.sentiment.polarity)
        
        self.get_avg_polarity(polarity_list)
        self.tweets_analyzed = True
        return polarity_list
    
    def get_avg_polarity(self, polarity_list):
        """
        After analysing all tweets and writing a polarity row to the dataframe (and to the csv) calculate the avg_polarity and get its textual output
        """
        avg_polarity = np.mean(polarity_list)
        avg_polarity_meaning = self.get_polarity_meaning(avg_polarity)
        self.get_avg_polarity = avg_polarity_meaning  # or should i put avg_polarity as number from -1 to 1 in here and change output in menu
        print("The average polarity of your topic is: ", f"'{avg_polarity_meaning}'")


    def analyse_single_tweet(self, index):
        """
        analyse Polarity of single tweet.
        """
        tweet_text = self.tweets[index]
        cleaned_tweet_text = self.clean_tweet(tweet_text)
        analysis = textblob.TextBlob(cleaned_tweet_text)
        return self.get_polarity_meaning(analysis.sentiment.polarity)

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
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.figure()
        plt.imshow(twitter_mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        
        #img = Image.open("wordcloud/generated/twitterlogo_wc.png")
        #img.show()










        




    