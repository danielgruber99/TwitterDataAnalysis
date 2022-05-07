import pandas as pd
import src.constants as const
from collections import Counter, Iterable

from funcy import flatten, isa

class DataProcessing:
    """
    Class for processing data, getting hashtags on so forth, also fetching followers/profiles of given users
    """
    def __init__(self, querystring):
        self.querystring = querystring
        self.csv_file = f"fetched/{self.querystring}/{self.querystring}.csv"
        self.csv_file_users = f"fetched/{self.querystring}/users.csv"
        self.tweets_df = self.read_csv_file()

    def read_csv_file(self):
        return pd.read_csv(self.csv_file, lineterminator='\n')
    
    def get_users(self) -> list:
        return self.tweets_df[const.user_id]
    
    def get_hashtags(self) -> list:
        return self.tweets_df['hashtags']

    def get_top_10_hashtags(self):
        hashtags = list(self.get_hashtags())
        #print(hashtags)
        hashtags_flat = self.flatten_list(hashtags)
        print(hashtags_flat)
        #c = Counter(hashtags_flat)
        #top_10_hashtags = c.most_common(10)
        #print("Top 10 Hashtags based on frequency: ")

        #for i in range(10):
        #    print(f"{i+1}.:", "#"+top_10_hashtags[i][0])

    def get_top_10_users(self):
        users = list(self.get_users())
        print(users)

        c = Counter(users)
        top_10_users = c.most_common(10)
        print("Top 10 Users based on number of tweets in acquired data set: ")

        for i in range(10):
            print(f"{i+1}.:", top_10_users[i][0], "with", top_10_users[i][1], "tweets.")

    def flatten_list(self, nestedList):
        nonListElems=[]
        listElems=[]
        nestedListCounter=0
        for nc in range(len(nestedList)):
            if type(nestedList[nc])==list:
                nestedListCounter+=1
                listElems=nestedList[nc]+listElems
            else:nonListElems.append(nestedList[nc])  
        if nestedListCounter==0: return (nestedList)
        else:
            nestedList=listElems+nonListElems 
            return self.flatten_list(nestedList)


        #print(users)
        #group_users = self.tweets_df.groupby(by=const.user_id).size()
        #print(type(group_users))
        #group_users = sorted(group_users)
        #print(group_users)




    
        


