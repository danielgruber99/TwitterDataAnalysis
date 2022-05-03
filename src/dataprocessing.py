import pandas as pd


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
        return self.tweets_df["user_id"]
    
    def get_top_10_users(self):
        users = self.get_users()
        print(users)
        group_users = self.tweets_df.groupby(by='user_id').size()
        print(type(group_users))
        group_users = sorted(group_users)
        print(group_users)


    
        


