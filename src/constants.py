# constants

# --------------------------------------------------------
# dataframe tweets
tweet_id = "Tweet ID"
tweet_text = "Tweet text"
tweet_entities = "Tweet entities"
tweet_createdAt = "Tweet created at"
tweet_hashtags = "hashtags"

# --------------------------------------------------------
# dataframe users
user_id = "User ID"
user_name = "name"
user_username = "username"

# --------------------------------------------------------
# dataframe followers
follower_id = "Follower ID"
follower_name = "name"
follower_username = "username"
follower_bio = "bio"
follower_location = "location"
follower_created_at = "created_at"
follower_public_metrics = "Public Metrics"
follower_following = "Following"
follower_followers = "Followers"
follower_url = "URL"
follower_profile_image_url = "profile image url"

# dataframe followers_tweets
# follower_id as in dataframe followers
follower_tweet_id = "Tweet ID"
follower_tweet_text = "Tweet text"

# --------------------------------------------------------
# number of shown entries per page
NR_ENTRIES_PAGE = 20
# Number of tweets to fetch
NR_TWEETS = 100
# Number of followers of given userid to fetch
NR_FOLLOWERS = 500

# Number of followers to fetch tweets for (only those first followers are considered and tweets are fetched only for those)
NR_FOLLOWERS_FOR_TWEETS = 50 - 1  # as indexing begins from zero, 0 - 49 are 50 elements
# Number of followers tweets to fetch
NR_FOLLOWERS_TWEETS = 20
