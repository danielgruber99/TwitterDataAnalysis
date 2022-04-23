import tweepy


client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAABqKbgEAAAAAS2RKvDrWSBI4OGvmZz8Qqe%2Bmg%2F0%3D20aat5g0H71Cj1yiBDTyAJSENfzO3cYZ3VWCJfnWywIC7OiIZz",
consumer_key = "fm0EuJ83rk0r843ibjlGnTiW4",
consumer_secret = "0O0viPgphDri25PdwWqjf1RED6mmfxDqfXeWBDYqDcouLPPooA",
access_token = "2904125878-WGdmAvONtSBtaoebTKu98ut9qDCeIi66FJrBCkL",
access_token_secret="Xad9Ny5BgL6icB4hPC3ggQIodU9QmernG8ibpI1Flqr0q")


tweets = client.search_recent_tweets(query="soccer", max_results=10)
print(tweets)

#auth = tweetpy.OAuthHandler(consumer_key, consumer_api, callback_uri)
#redirect_url = auth.get_authorization_url()
#webbrowser.open(redirect_url)

#auth = tweepy.OAuth2BearerHandler('AAAAAAAAAAAAAAAAAAAAABqKbgEAAAAAS2RKvDrWSBI4OGvmZz8Qqe%2Bmg%2F0%3D20aat5g0H71Cj1yiBDTyAJSENfzO3cYZ3VWCJfnWywIC7OiIZz')
#api = tweepy.api(auth)



