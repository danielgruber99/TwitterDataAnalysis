from matplotlib.colors import TwoSlopeNorm
from simple_term_menu import TerminalMenu
import pandas as pd
import time
import threading
import keyboard as kb

from src.sentimentanalysis import SentimentAnalysis
from src.dataprocessing import DataProcessing
import src.constants as const

class Menu:
    """
    This class handles the menu and provides to user a simple user interface in the command line. (Implemented with simple_term_menu)
    """
    def __init__(self, twitterclient_v2):
        # main menu
        self.main_menu_exit = False
        self.main_menu = None
        # submenu0
        self.submenu_0_exit = False
        self.submenu_0 = None
        # submenu1
        self.submenu_1_exit = False
        self.submenu_1 = None
        # submenu2
        self.submenu_2_exit = False
        self.submenu_2 = None
        # Client, qerystring and startmenu
        self.twitterclient_v2 = twitterclient_v2
        self.querystring = twitterclient_v2.querystring
        self.tweets_df = None
        self.tweets_users = None
        self.sentimentanalysis = SentimentAnalysis(self.querystring)
        self.dataprocessing = DataProcessing(self.querystring)

        # setup main_menu and all submenus
        self._setup_submenu0()
        self._setup_submenu1()
        self._setup_submenu2()
        self._setup_main_menu()
        # start menu loop
        self._menu_selection_loop()


    def _setup_main_menu(self):
        """
        Main Menu.
        """
        header = "=============================Twitter Data Analysis=========================="
        topic = "Topic: " + self.querystring
        title = header + "\n" + topic
        choices = ["[0] Browse Tweets/Users", "[1] Analyse Sentiment of Tweets", "[2] Get Top 10 Hashtags/Users", "[3] Get followers of given twitter user", 
        "[4] Obtain tweets and profiles of followers of given twitter user","[c] change Topic", "[q] Quit"]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.main_menu = TerminalMenu(
            menu_entries = choices,
            title = title,
            menu_cursor = cursor,
            menu_cursor_style = cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def _setup_submenu0(self):
        """
        Submenu 00 for browsing Tweets/Users.
        """
        title="========================Submenu 00: Browse Tweets/Users====================="
        choices = ["[0] Browse Tweets.", "[1] Browse Users.", "[2] Get Markdown of Tweets and Users.", "[b] Back."]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_0 = TerminalMenu(
            menu_entries = choices,
            title = title,
            menu_cursor = cursor,
            menu_cursor_style = cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def _setup_submenu1(self):
        """
        Submenu 01 for Sentiment Analysis.
        """
        title="========================Submenu 01: sentimentanalysis====================="
        choices = ["[0] Analyse all tweets and get avg Polarity", "[1] Analyse single tweet", "[2] Get most used words.", "[b] Back."]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_1 = TerminalMenu(
            menu_entries = choices,
            title = title,
            menu_cursor = cursor,
            menu_cursor_style = cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )
    
    def _setup_submenu2(self):
        """
        Submenu 02 for getting Top 10 Hashtags/Users.
        """
        title="========================Submenu 02: Get Top 10 Hashtags/Users====================="
        choices = ["[0] Get Top 10 Hashtags", "[1] Get Top 10 Users", "[b] Back."]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_2 = TerminalMenu(
            menu_entries = choices,
            title = title,
            menu_cursor = cursor,
            menu_cursor_style = cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )
    
    


    def _menu_selection_loop(self):
        # for default case
        self.tweets_df = pd.read_csv(f'fetched/{self.querystring}/{self.querystring}.csv', lineterminator='\n')
        
        while not self.main_menu_exit:
            # main menu
            main_sel = self.main_menu.show()

            # [0] Browse Tweets/Users
            # TODO: utilize keyboard library, alread imported above as kb
            if main_sel == 0:
                while not self.submenu_0_exit:
                    submenu_0_sel = self.submenu_0.show()
                    # browse Tweets
                    if submenu_0_sel == 0:
                        start_browse_tweets = 0
                        browse_tweets_exit = False
                        while not browse_tweets_exit:
                            print(f"Tweets {start_browse_tweets} to {start_browse_tweets+10}", self.tweets_df[start_browse_tweets:start_browse_tweets+10])
                            other_input = input("Press n/p to get next/previous 10 tweets. Press b to go back to the main menu. ")
                            if other_input == 'n':
                                start_browse_tweets+=10
                            elif other_input == 'p':
                                if start_browse_tweets-10 >=0:
                                    start_browse_tweets-=10
                            elif other_input == 'b':
                                browse_tweets_exit = True
                            else:
                                print("Input not valid.")
                        browse_tweets_exit=False
                    # browse Users
                    elif submenu_0_sel == 1:
                        pass
                    # get markdown
                    elif submenu_0_sel == 2:
                        self.tweets_df.to_markdown(f"fetched/{self.querystring}/tweets_markdown.md")
                        print(f"Files are stored at fetched/{self.querystring}/")
                        input("Press enter to continue...")
                    elif submenu_0_sel == 'b' or submenu_0_sel == 3:
                        self.submenu_0_exit = True
                self.submenu_0_exit = False
                    
            # [1] Analyse Sentiment of Tweets
            elif main_sel == 1:
                # submenu 1
                while not self.submenu_1_exit:
                    submenu_1_sel = self.submenu_1.show()
                    if submenu_1_sel == 0:
                        self.sentimentanalysis.analyse_all_tweets()
                        time.sleep(5)
                    elif submenu_1_sel == 1:
                        print(self.tweets_df[0:10])
                        index = self.get_TwitterID_to_analyse()
                        polarity_meaning = self.sentimentanalysis.analyse_single_tweet(index)
                        print("Your selected Tweet at index", index, "is", polarity_meaning)
                        time.sleep(3)
                    elif submenu_1_sel == 2:
                        self.sentimentanalysis.get_most_used_words()
                        print("file is in wordcloud/generated")
                        time.sleep(3)
                    elif submenu_1_sel == 'b' or submenu_1_sel == 3:
                        self.submenu_1_exit = True
                        #print("back selected")
                        #time.sleep(0.5)
                self.submenu_1_exit = False

            # [2] Get Top 10 Hashtags/Users
            elif main_sel == 2:
                # submenu 2
                while not self.submenu_2_exit:
                    submenu_2_sel = self.submenu_2.show()
                    # Get Top 10 Hashtags
                    if submenu_2_sel == 0:
                        self.dataprocessing.get_top_10_hashtags()
                        time.sleep(3)
                    # Get Top 10 Users
                    elif submenu_2_sel == 1:
                        self.dataprocessing.get_top_10_users()
                        time.sleep(3)
                    # back
                    elif submenu_2_sel == 'b' or submenu_2_sel == 2:
                        self.submenu_2_exit = True
                        print("back selected")
                        time.sleep(1)
                self.submenu_2_exit = False
            
            # [3] Get followers of given twitter user
            elif main_sel == 3:
                print(self.tweets_df[0:20])
                print("Enter a twitter user: ")
                userid = self.get_userid()

                if userid != -1:
                    followers_df = self.twitterclient_v2.get_followers(userid)
                else:
                    print("Your input does not match any user in this dataset. Please enter a user available in this data set.")
                start_browse_followers = 0
                browse_followers_exit = False
                while not browse_followers_exit:
                    print(f"Followers {start_browse_followers} to {start_browse_followers+10}",followers_df[start_browse_followers:start_browse_followers+20])
                    browse_followers_input = input("Press n/p to get next/previous 20 followers. Press b to go back to the main menu. ")
                    if browse_followers_input == 'n':
                        start_browse_followers+=20
                    elif browse_followers_input == 'p':
                        if start_browse_followers-20 >=0:
                            start_browse_followers-=20
                    elif browse_followers_input == 'b':
                        browse_followers_exit = True
                    else:
                        print("Input not valid.")
                browse_followers_exit = False

            # [4] obtain tweets and profiles of followers of given twitter user
            elif main_sel == 4:
                print(self.tweets_df[0:20])
                print("Enter a twitter user: ")
                userid = self.get_userid()
                if userid != -1:
                    username = self.twitterclient_v2.lookup_user(userid)
                else:
                    pass
                
                print(username)
                time.sleep(4)
                
            
            # [c] change Topic
            elif main_sel == 5 or main_sel == 'c':
                print("Current Topic is:", self.querystring)
                self.querystring = self.get_querystring_from_user()
                self._setup_main_menu() # setup main menu new, so that topic refreshes
                self.twitterclient_v2.get_tweets(self.querystring)
                self.sentimentanalysis = SentimentAnalysis(self.querystring)
                self.dataprocessing = DataProcessing(self.querystring)
                self.tweets_df = pd.read_csv(f'fetched/{self.querystring}/{self.querystring}.csv', lineterminator='\n')
                
            # [q] Quit
            elif main_sel == 6 or main_sel == 'q':
                self.main_menu_exit = True
                print("You quit!")

    def get_TwitterID_to_analyse(self):
        twitterid = int(input("Enter Tweet ID or Index of the Tweet to analyse: "))
        if self.check_twitterid_exists(twitterid):
            return twitterid
        else:
            return -1

    def get_userid(self):
        userid = int(input("Enter User ID: "))
        if self.check_userid_exists(userid):
            if userid in self.dataprocessing.get_users_without_duplicates():
                return userid
            else:
                return self.tweets_df[const.user_id][userid]
        else:
            return -1

    def check_twitterid_exists(self, twitterid):
        tweets = self.dataprocessing.get_tweets()
        if twitterid in tweets or twitterid < self.tweets_df.shape[0]:
            return True
        return False

    def check_userid_exists(self, userid):
        users = self.dataprocessing.get_users_without_duplicates()
        if userid in users or userid < self.tweets_df.shape[0]:
            return True
        return False
    

    def get_querystring_from_user(self):
        #Input from the User
        choice = input("Enter your querystring: ")
        return choice

