import pandas as pd
from collections import Counter, Iterable
import src.constants as const


class DataProcessing:
    """
    Class for processing data, getting hashtags on so forth, also fetching followers/profiles of given users
    """
    def __init__(self, querystring):
        self.querystring = querystring
        self.csv_file_tweets = f"fetched/{self.querystring}/{self.querystring}.csv"
        self.csv_file_users = f"fetched/{self.querystring}/users.csv"
        self.tweets_df = self.read_csv_file_tweets()
        self.users_df = None#self.read_csv_file_users()

    def read_csv_file_tweets(self)->pd.DataFrame:
        """
        Read csv file for tweets into pandas dataframe and return it.
        """
        return pd.read_csv(self.csv_file_tweets, lineterminator='\n')
    
    def read_csv_file_users(self)->pd.DataFrame:
        """
        Read csv file for users into pandas dataframe and return it.
        """
        return pd.read_csv(self.csv_file_users, lineterminator='\n')
    
    def get_users(self) -> list:
        """
        Get all users (can contain duplicates).
        """
        return list(self.tweets_df[const.user_id])
    
    def get_users_without_duplicates(self)->list:
        """
        Get users without duplicates.
        """
        return list(set(self.get_users()))
    
    def get_tweets_id(self) -> list:
        """
        Get tweet IDs.
        """
        return list(self.tweets_df[const.tweet_id])
    
    def get_tweets_text(self) -> list:
        """
        Get tweet texts.
        """
        return list(self.tweets_df[const.tweet_text])
    
    def get_hashtags(self) -> list:
        """
        Get hashtags.
        """
        return list(self.tweets_df[const.tweet_hashtags])

    def get_top_10_hashtags(self)->list:
        """
        Determine top 10 most used Hashtags.

        Returns
        -------
        top_10_hashtags:    a list of tuples (hashtag, occurences), which contains the 10 most used hashtags
        """
        # join every element of the list with ',', as also the hashtags in one element are stored as , separated list
        all_hashtags = ','.join(self.get_hashtags())
        # get all hashtags as list by splitting those by ','
        hashtag_list = all_hashtags.split(',')
        c = Counter(hashtag_list)
        top_10_hashtags = c.most_common(10)
        return top_10_hashtags
    
    def get_top_10_users(self)->list:
        """
        Determine top 10 Users based on their number of Tweets.

        Returns
        -------
        top_10_users:    a list of tuples (userid, occurences), which contains the 10 users with most Tweets
        """
        users = self.get_users()
        c = Counter(users)
        top_10_users = c.most_common(10)
        return top_10_users
