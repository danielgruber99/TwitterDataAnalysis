"""
Twitterclient module for connecting to the Twitter API Endpoint.
Client is used for fetching tweets, users, followers and tweets of followers.
"""
import os
import tweepy
import pandas as pd
import src.constants as const


class TwitterClient:
    """
    This class is used to firstly create a connection to the Twitter API v2 Endpoint by authenticating
    with required tokens. After the successful creation of the client connection it provides several
    methods to fetch tweets, users, followers and the tweets of followers.

    Attributes
    ----------
    client : tweepy.Client
    """

    def __init__(self):
        """
        Authenticate to the twitter API v2 endpoint.
        """
        self.client = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticate to twitter API v2 endpoint by setting the member variable client.
        """
        bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        # logon to api v2 endpoint
        try:
            self.client = tweepy.Client(bearer_token=bearer_token)
        except:
            self.client = None
            print("Error: Authentication Failed!")

    def fetch_tweets(self, querystring) -> pd.DataFrame:
        """
        Fetch Tweets for given querystring where only tweets in language english with at least one hashtag are considered. Retweets are excluded.

        Parameters
        ----------
        querystring : str
            the topic (querystring) for which tweets is searched to fetch

        Returns
        -------
        tweets_df : pd.DataFrame or None
            Contains fetched tweets, or None if an error/exception occured.
        """
        tweets_df = None
        if self.client:
            try:
                response = self.client.search_recent_tweets(
                    query=f"{querystring} lang:en -is:retweet has:hashtags",
                    tweet_fields=["created_at", "lang", "entities"],
                    expansions=["author_id"],
                    max_results=const.NR_TWEETS,
                )
                columns = [
                    const.tweet_id,
                    const.tweet_text,
                    const.tweet_hashtags,
                    const.tweet_createdAt,
                    const.user_id,
                ]
                data = []
                for tweet in response.data:
                    hashtags = self.extract_hashtags(tweet)
                    data.append(
                        [
                            tweet.id,
                            tweet.text,
                            hashtags,
                            tweet.created_at,
                            tweet.author_id,
                        ]
                    )
                    tweets_df = pd.DataFrame(data, columns=columns)
            except tweepy.errors.Unauthorized as unauthorized:
                print("Unauthorized:", unauthorized)
                print(
                    "Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
                )
            except tweepy.errors.TooManyRequests as toomanyrequests:
                print("TooManyRequests:", toomanyrequests)
                print(
                    "You have done too many requests. Try again in approximately 15 minutes."
                )
        else:
            print(
                "The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
            )
        return tweets_df

    def fetch_users(self, userids) -> pd.DataFrame:
        """
        Fetch User IDs, names and usernames of given userids in previously fetched set of Tweets.
        Required for providing the user the possibility to browse through all users.

        Parameters
        ----------
        userids : list
            userids to look up the name and username for

        Returns
        -------
        users_df : pd.DataFrame or None
            Contains fetched users, or None if an error/exception occured.
        """
        columns = [const.user_id, const.user_name, const.user_username]
        data = []
        if self.client:
            for userid in userids:
                try:
                    response = self.client.get_user(
                        id=userid, user_fields=["id", "name", "username"]
                    )
                    user = response.data
                    # handle if for user no data could be fetched but also no error was trown by the Twitter API
                    if user:
                        data.append([user.id, user.name, user.username])
                except tweepy.errors.Unauthorized as unauthorized:
                    print("Unauthorized:", unauthorized)
                    print(
                        "Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
                    )
                    return None
                except tweepy.errors.TooManyRequests as toomanyrequests:
                    print("TooManyRequests:", toomanyrequests)
                    print(
                        "You have done too many requests. Try again in approximately 15 minutes."
                    )
                    return None
        else:
            print(
                "The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
            )
            return None
        users_df = pd.DataFrame(data, columns=columns)
        return users_df

    def extract_hashtags(self, tweet) -> list:
        """
        Extract hashtags from retrieved response.data dictionary.

        Parameters
        ----------
        tweet : str
            userids to look up the name and username for

        Returns
        -------
        hashtags_string : str
            string of all hashtags separated by commas (for later splitting again)
        """
        entity_hashtag = tweet.entities["hashtags"]
        hashtags = []
        for hashtag in entity_hashtag:
            hashtags.append(hashtag["tag"])
        hashtags_string = ",".join(hashtags)
        return hashtags_string

    def fetch_followers(self, userid) -> pd.DataFrame:
        """
        Fetch followers for a given user ID.

        Parameters
        ----------
        userid : int
            given userid to fetch followers for

        Returns
        -------
        followers_df : pd.DataFrame or None
            Contains fetched followers, or None if an error/exception occured.
        """
        followers_df = None
        if self.client:
            try:
                response_followers = self.client.get_users_followers(
                    userid,
                    user_fields=[
                        "created_at",
                        "description",
                        "entities",
                        "id",
                        "location",
                        "name",
                        "profile_image_url",
                        "public_metrics",
                        "url",
                        "username",
                    ],
                    max_results=const.NR_FOLLOWERS,
                )
            except tweepy.errors.Unauthorized as unauthorized:
                print("Unauthorized:", unauthorized)
                print(
                    "Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
                )
            except tweepy.errors.TooManyRequests as toomanyrequests:
                print("TooManyRequests:", toomanyrequests)
                print(
                    "You have done too many requests. Try again in approximately 15 minutes."
                )
            else:
                followers = response_followers.data
                columns = [
                    const.follower_id,
                    const.follower_name,
                    const.follower_username,
                    const.follower_bio,
                    const.follower_location,
                    const.follower_url,
                    const.follower_created_at,
                    const.follower_following,
                    const.follower_followers,
                    const.follower_profile_image_url,
                ]  # description in user is better known as bio (profile of user)
                data = []
                if followers:
                    for follower in followers:
                        data.append(
                            [
                                follower.id,
                                follower.name,
                                follower.username,
                                follower.description,
                                follower.location,
                                follower.url,
                                follower.created_at,
                                follower.public_metrics.get("following_count"),
                                follower.public_metrics.get("followers_count"),
                                follower.profile_image_url,
                            ]
                        )
                    followers_df = pd.DataFrame(data, columns=columns)
        else:
            print(
                "The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
            )
        return followers_df

    def fetch_tweets_of_followers(self, followerids) -> pd.DataFrame:
        """
        Fetch tweets of given followers.

        Parameters
        ----------
        followerids : list
            Followerids to fetch tweets for.

        Returns
        -------
        followers_tweets_df : pd.DataFrame or None
            Contains fetched tweets for given list of followerids, or None if an error/exception occured.
        """
        columns = [
            const.follower_id,
            const.follower_tweet_id,
            const.follower_tweet_text,
        ]
        data = []
        if self.client:
            for followerid in followerids:
                try:
                    response = self.client.get_users_tweets(
                        followerid, max_results=const.NR_FOLLOWERS_TWEETS
                    )
                except tweepy.errors.Unauthorized as unauthorized:
                    print("Unauthorized:", unauthorized)
                    print(
                        "Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
                    )
                    return None
                except tweepy.errors.TooManyRequests as toomanyrequests:
                    print("TooManyRequests:", toomanyrequests)
                    print(
                        "You have done too many requests. Try again in approximately 15 minutes."
                    )
                    return None
                else:
                    tweets_of_followers = response.data
                    if tweets_of_followers is not None:
                        for follower_tweet in tweets_of_followers:
                            data.append(
                                [followerid, follower_tweet.id, follower_tweet.text]
                            )
        else:
            print(
                "The twitterclient couldn't be set up.\nEnsure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
            )
        followers_tweets_df = pd.DataFrame(data, columns=columns)
        return followers_tweets_df

    def lookup_user(self, userid) -> str:
        """
        Lookup username for given user ID.

        Parameters
        ----------
        userid : int
            userid to lookup corresponding username.

        Returns
        -------
        user.username : str or None
            Contains username of given userid, or None if an error/exception occured.
        """
        if self.client:
            try:
                response = self.client.get_user(
                    id=userid, user_fields=["name", "username"]
                )
            except tweepy.errors.Unauthorized as unauthorized:
                print("Unauthorized:", unauthorized)
                print(
                    "Authorization failed. Ensure you have provided valid Access/Consumer/Bearer Tokens and Secrets."
                )
            except tweepy.errors.TooManyRequests as toomanyrequests:
                print("TooManyRequests:", toomanyrequests)
                print(
                    "You have done too many requests. Try again in approximately 15 minutes."
                )
            else:
                user = response.data
                if user:
                    return user.username
        else:
            return None
