import pandas as pd
import src.constants as const
from collections import Counter, Iterable


class DataProcessing:
    """
    Class for processing data, getting hashtags on so forth, also fetching followers/profiles of given users
    """
    def __init__(self, querystring):
        self.querystring = querystring
        self.csv_file = f"fetched/{self.querystring}/{self.querystring}.csv"
        self.csv_file_users = f"fetched/{self.querystring}/users.csv"
        self.tweets_df = self.read_csv_file()

    def read_csv_file(self)->pd.DataFrame:
        """
        Read csv file into pandas dataframe and return dataframe.
        """
        return pd.read_csv(self.csv_file, lineterminator='\n')
    
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

    def get_top_10_hashtags(self):
        hashtags = list(self.get_hashtags())
        all_hashtags = ','.join(hashtags)
        print(all_hashtags)
        hashtag_list = all_hashtags.split(',')
        print(hashtag_list)

        c = Counter(hashtag_list)
        top_10_hashtags = c.most_common(10)
        print("Top 10 Hashtags based on frequency: ")

        for i in range(10):
            print(f"{i+1}.:", "#"+top_10_hashtags[i][0])
    

    def get_top_10_users(self):
        users = list(self.get_users())
        print(users)

        c = Counter(users)
        top_10_users = c.most_common(10)
        print("Top 10 Users based on number of tweets in acquired data set: ")

        for i in range(10):
            print(f"{i+1}.:", top_10_users[i][0], "with", top_10_users[i][1], "tweets.")


