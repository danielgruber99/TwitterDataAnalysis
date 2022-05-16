import pandas as pd
import src.constants as const
from collections import Counter, Iterable


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
        Read csv file into pandas dataframe and return dataframe.
        """
        return pd.read_csv(self.csv_file_tweets, lineterminator='\n')
    
    def read_csv_file_users(self)->pd.DataFrame:
        """
        Read csv file into pandas dataframe and return dataframe.
        """
        return pd.read_csv(self.csv_file_users, lineterminator='\n')
    
    def get_users(self) -> list:
        """
        Get all users (can contain duplicates).
        """
        return self.tweets_df[const.user_id]
    
    def get_users_without_duplicates(self)->list:
        """
        Get users without duplicates.
        """
        return list(set(self.get_users()))
    
    def get_tweets(self) -> list:
        return self.tweets_df[const.tweet_id]
    
    def get_hashtags(self) -> list:
        return self.tweets_df['hashtags']

    def get_top_10_hashtags(self)->list:
        """
        Determine top 10 most used Hashtags.

        Returns
        -------
        top_10_hashtags:    a list of tuples (hashtag, occurences), which contains the 10 most used hashtags
        """
        hashtags = list(self.get_hashtags())
        all_hashtags = ','.join(hashtags)
        #print(all_hashtags)
        hashtag_list = all_hashtags.split(',')
        #print(hashtag_list)
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
        users = list(self.get_users())
        #print(users)
        c = Counter(users)
        top_10_users = c.most_common(10)
        return top_10_users


