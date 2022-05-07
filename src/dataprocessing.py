import pandas as pd
import src.constants

class DataProcessing:
    """
    Class for processing data, getting hashtags on so forth, also fetching followers/profiles of given users
    """
    def __init__(self, querystring):
        self.querystring = querystring
        self.csv_file = f"fetched/{self.querystring}/{self.querystring}.csv"
        self.tweets_df = self.read_csv_file()

    def read_csv_file(self):
        return pd.read_csv(self.csv_file, lineterminator='\n')
    
    def get_users(self) -> list:
        return self.tweets_df[const.user_id]
    
    def get_hashtags(self) -> list:
        return self.tweets_df[const.tweet_entities]

    def get_top_10_users(self):
        users = self.get_users()
        print(users)
        group_users = self.tweets_df.groupby(by=const.user_id).size()
        print(type(group_users))
        group_users = sorted(group_users)
        print(group_users)


    
        


