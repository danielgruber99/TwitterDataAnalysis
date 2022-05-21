from src.sentimentanalysis import SentimentAnalysis
from src.twitterclient import TwitterClient
from src.menu import Menu
from src.dataprocessing import DataProcessing

def main():
    # prefetch of topic computer
    default_topic = "computer"
    twitterclient = TwitterClient()  
    twitterclient.fetch_tweets(default_topic)


    ## TODO: how to get those classes in functionality separeted. (Separation of INterest/Concepts)
    # setup dataprocessing class
    #dataprocessing = DataProcessing(default_topic)
    # init sentimentanalysis class
    #sentimentanalysis = SentimentAnalysis(dataprocessing.get_tweets)


    #-----------------------------------------------------------------------
    # START MENU
    myMenu = Menu(twitterclient)        


if __name__ == "__main__":
    main()

