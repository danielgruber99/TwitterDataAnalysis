from src.sentimentanalysis import SentimentAnalysis
from src.twitterclient_v2 import TwitterClient_v2
from src.menu import Menu
from src.dataprocessing import DataProcessing

def main():
    # prefetch of topic computer
    default_topic = "computer"
    twitterclient_v2 = TwitterClient_v2()  
    twitterclient_v2.fetch_tweets(default_topic)


    ## TODO: how to get those classes in functionality separeted. (Separation of INterest/Concepts)
    # setup dataprocessing class
    #dataprocessing = DataProcessing(default_topic)
    # init sentimentanalysis class
    #sentimentanalysis = SentimentAnalysis(dataprocessing.get_tweets)


    #-----------------------------------------------------------------------
    # START MENU
    myMenu = Menu(twitterclient_v2)        


if __name__ == "__main__":
    main()

