"""
Dataprocessing module for getting dataframes, generating markdowns, loading only certain columns of dataframes.
"""
import os.path
import pandas as pd
import src.constants as const
from collections import Counter
from src.twitterclient import TwitterClient


class DataProcessing:
    """
    This class handles all kind of dataprocessing. It is responsible for Getting required dataframes of tweets, users,
    followers and tweets_of_followers. This includes fetching the data with the twitterclient if not stored in fetched.
    If it is stored in fetched the class will only read those csv into pandas dataframes.
    Moreover getting only one column of certain dataframes is possible.

    Parameters
    ----------
    querystring : str

    Attributes
    ----------
    querystring : str
    csv_file_tweets : str
    csv_file_users : str
    csv_file_followers_path : str
    twitterclient : TwitterClient
    tweets_df : pd.DataFrame
    users_df : pd.DataFrame
    followers_df : pd.DataFrame
    Followers_Tweets_df : pd.DataFrame
    """

    def __init__(self, querystring):
        """
        Constructor for DataProcessing setting up the file paths correctly. Also instantiates the TwitterClient instance.
        """
        self.querystring = querystring
        # file paths
        self.csv_file_tweets = f"fetched/{self.querystring}/{self.querystring}.csv"
        self.csv_file_users = f"fetched/{self.querystring}/{self.querystring}_users.csv"
        self.csv_file_followers_path = f"fetched/{self.querystring}/followers"
        # create querystring, followers and markdown folder
        self.create_folder(f"fetched/{self.querystring}")
        self.create_folder(f"fetched/{self.querystring}/followers")
        self.markdown_folder = f"fetched/{self.querystring}/markdown"
        self.create_folder(self.markdown_folder)
        # f"{self.csv_folder_path}followers/{userid}_followers.csv")
        # followers_tweets_df.to_csv(f"{self.csv_folder_path}followers/{userid}_followers_tweets.csv")
        # twitterclient
        self.twitterclient = TwitterClient()
        # dataframes
        self.tweets_df = None
        self.users_df = None
        self.followers_df = None
        self.followers_tweets_df = None

    def create_folder(self, folder):
        """
        For each querystring a dedicated folder will be created under 'fetched/'. This function will check if the folder already exists and, if not, creates it.

        Parameters
        ----------
        folder : str
            The folder to create.
        """
        folder = folder
        CHECK_FOLDER = os.path.isdir(folder)

        if not CHECK_FOLDER:
            os.makedirs(folder)
        else:
            pass

    def generate_tweets_df_md_file(self):
        """
        Generate tweets_df markdown file if not already generated and show the user the file path.
        """
        tweets_df_md_path = f"{self.markdown_folder}/tweets_markdown.md"
        if not os.path.exists(tweets_df_md_path):
            self.tweets_df.to_markdown(tweets_df_md_path)
        print(f"Markdown file is stored at {tweets_df_md_path}.")

    def generate_users_df_md_file(self):
        """
        Generate users_df markdown file if not already generated and show the user the file path.
        """
        users_df_md_path = f"{self.markdown_folder}/users_markdown.md"
        if not os.path.exists(users_df_md_path):
            self.users_df.to_markdown(users_df_md_path)
        print(f"Markdown file is stored at {users_df_md_path}.")

    def generate_followers_df_md_file(self, userid):
        """
        Generate followers_df markdown file if not already generated and show the user the file path.
        """
        followers_df_md_path = f"{self.markdown_folder}/{userid}_followers_markdown.md"
        if not os.path.exists(followers_df_md_path):
            self.followers_df.to_markdown(followers_df_md_path)
        print(f"Markdown file is stored at {followers_df_md_path}.")

    def generate_followers_tweets_df_md_file(self, userid):
        """
        Generate followers_tweets_df markdown file if not already generated and show the user the file path.
        """
        followers_tweets_df_md_path = (
            f"{self.markdown_folder}/{userid}_followers_tweets_markdown.md"
        )
        if not os.path.exists(followers_tweets_df_md_path):
            self.followers_tweets_df.to_markdown(followers_tweets_df_md_path)
        print(f"Markdown file is stored at {followers_tweets_df_md_path}.")

    def get_tweets_df(self) -> pd.DataFrame:
        """
        Get tweets dataframe either by reading csv file if it exists or fetch with twitterclient.

        Returns
        -------
        tweets_df : pd.DataFrame or None
            DataFrame containing tweets, or None if an error occured.
        """
        if self.tweets_df is None:
            if os.path.exists(self.csv_file_tweets):
                self.tweets_df = pd.read_csv(self.csv_file_tweets, lineterminator="\n")
            else:
                self.tweets_df = self.twitterclient.fetch_tweets(self.querystring)
                if self.tweets_df is not None:
                    self.tweets_df.to_csv(self.csv_file_tweets)
        return self.tweets_df

    def get_users_df(self) -> pd.DataFrame:
        """
        Get users dataframe either by reading csv file if it exists or fetch with twitterclient.

        Returns
        -------
        users_df : pd.DataFrame or None
            DataFrame containing users, or None if an error occured.
        """
        if self.users_df is None:
            if os.path.exists(self.csv_file_users):
                self.users_df = pd.read_csv(self.csv_file_users, lineterminator="\n")
            else:
                users_without_duplicates = self.get_user_ids_without_duplicates()
                self.users_df = self.twitterclient.fetch_users(users_without_duplicates)
                if self.users_df is not None:
                    self.users_df.to_csv(self.csv_file_users)
        return self.users_df

    def get_followers_df(self, userid) -> pd.DataFrame:
        """
        Get followers dataframe either by reading csv file if it exists or fetch with twitterclient.

        Parameters
        ----------
        userid : int
            For loading the correct followers dataframe.

        Returns
        -------
        followers_df : pd.DataFrame or None
            DataFrame containing followers for given userid, or None if an error occured.
        """
        self.followers_df = None
        if os.path.exists(f"{self.csv_file_followers_path}/{userid}_followers.csv"):
            self.followers_df = pd.read_csv(
                f"{self.csv_file_followers_path}/{userid}_followers.csv",
                lineterminator="\n",
            )
        else:
            self.followers_df = self.twitterclient.fetch_followers(userid)
            if self.followers_df is not None:
                self.followers_df.to_csv(
                    f"{self.csv_file_followers_path}/{userid}_followers.csv"
                )
        return self.followers_df

    def get_followers_tweets_df(self, userid) -> pd.DataFrame:
        """
        Get follower_tweets dataframe either by reading csv file if it exists or fetch with twitterclient.

        Parameters
        ----------
        userid : int
            For loading the correct followers_tweets dataframe.

        Returns
        -------
        followers_tweets_df : pd.DataFrame or None
            DataFrame containing Tweets of followers for given userid, or None if an error occured.
        """
        self.followers_tweets_df = None
        if os.path.exists(
            f"{self.csv_file_followers_path}/{userid}_followers_tweets.csv"
        ):
            self.followers_tweets_df = pd.read_csv(
                f"{self.csv_file_followers_path}/{userid}_followers_tweets.csv",
                lineterminator="\n",
            )
        else:
            if self.followers_df is None:
                self.get_followers_df(userid)
            # ensure that followers_df is not None, because get_followers_df(userid) could return None
            if self.followers_df is not None:
                followerids = self.followers_df[const.follower_id]
                # only fetch for first 50 followers tweets (but if less than 50 followers only less can be fetched, check this)
                nr_followers_to_fetch_tweets_for = (
                    const.NR_FOLLOWERS_FOR_TWEETS
                    if len(followerids) > const.NR_FOLLOWERS_FOR_TWEETS
                    else len(followerids) - 1
                )
                self.followers_tweets_df = self.twitterclient.fetch_tweets_of_followers(
                    followerids[0:nr_followers_to_fetch_tweets_for]
                )
                if self.followers_tweets_df is not None:
                    self.followers_tweets_df.to_csv(
                        f"{self.csv_file_followers_path}/{userid}_followers_tweets.csv"
                    )
        return self.followers_tweets_df

    def get_user_ids(self) -> list:
        """
        Get all user IDs (can contain duplicates).

        Returns
        -------
        list or None: userids existing in users_df dataframe potentially with duplicates, or None if an error occured.
        """
        if self.tweets_df is None:
            self.get_tweets_df()
        return list(self.tweets_df[const.user_id])

    def get_user_ids_without_duplicates(self) -> list:
        """
        Get user IDs without duplicates.

        Returns
        -------
        list or None: userids existing in users_df dataframe without duplicates, or None if an error occured.
        """
        if self.tweets_df is None:
            self.get_tweets_df()
        return list(set(self.tweets_df[const.user_id]))

    def get_tweets_id(self) -> list:
        """
        Get tweet ids.

        Returns
        -------
        list or None: tweet ids existing in tweets_df dataframe, or None if an error occured.
        """
        if self.tweets_df is None:
            self.get_tweets_df()
        # if not tweets_df could be fetched return none
        if self.tweets_df is None:
            return None
        return list(self.tweets_df[const.tweet_id])

    def get_tweets_text(self) -> list:
        """
        Get tweet texts.

        Returns
        -------
        list or None: tweet texts existing in tweets_df dataframe, or None if an error occured.
        """
        if self.tweets_df is None:
            self.get_tweets_df()
        # if not tweets_df could be fetched return none
        if self.tweets_df is None:
            return None
        return list(self.tweets_df[const.tweet_text])

    def get_hashtags(self) -> list:
        """
        Get hashtags.

        Returns
        -------
        list or None: hashtags existing in tweets_df dataframe, or None if an error occured.
        """
        if self.tweets_df is None:
            self.get_tweets_df()
        # if not tweets_df could be fetched return none
        if self.tweets_df is None:
            return None
        return list(self.tweets_df[const.tweet_hashtags])

    def get_top_10_hashtags(self) -> list:
        """
        Determine top 10 most used Hashtags.

        Returns
        -------
        top_10_hashtags : list or None
            a list of tuples (hashtag, occurences), which contains the 10 most used hashtags, or None if an error occured.
        """
        top_10_hashtags = None
        # join every element of the list with ',', as also the hashtags in one element are stored as ',' separated list
        hashtags = self.get_hashtags()
        if hashtags:
            all_hashtags = ",".join(hashtags)
            # get all hashtags as list by splitting those by ','
            hashtag_list = all_hashtags.split(",")
            c = Counter(hashtag_list)
            top_10_hashtags = c.most_common(10)
        return top_10_hashtags

    def get_top_10_users(self) -> list:
        """
        Determine top 10 Users based on their number of Tweets.

        Returns
        -------
        top_10_users : list or None
            a list of tuples (userid, occurences), which contains the 10 users with most Tweets, or None if an error occured.
        """
        top_10_users = None
        users = self.get_user_ids()
        if users:
            c = Counter(users)
            top_10_users = c.most_common(10)
        return top_10_users
