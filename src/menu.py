from matplotlib.colors import TwoSlopeNorm
from simple_term_menu import TerminalMenu
import pandas as pd
import time
import threading

from src.sentimentanalysis import SentimentAnalysis

class Menu:
    """
    This class handles the menu and provides to user a simple user interface in the command line. (Implemented with simple_term_menu)
    """
    def __init__(self, twitterclient_v2):
        # main menu
        self.main_menu_exit = False
        self.main_menu = None
        # submenu1
        self.submenu_1_exit = False
        self.submenu_1 = None
        # submenu2
        self.submenu_2_exit = False
        self.submenu_2 = None
        # Client, qerystring and startmenu
        self.twitterclient_v2 = twitterclient_v2
        self.querystring = twitterclient_v2.querystring
        self.sentimentanalysis = SentimentAnalysis(self.querystring)

        # setup main_menu and all submenus
        self._setup_submenu1()
        self._setup_submenu2()
        self._setup_main_menu()
        # start menu loop
        self._menu_selection_loop()


    def _setup_main_menu(self):
        header = "=============================Twitter Data Analysis=========================="
        topic = "Topic:" + self.querystring
        title = header + "\n" + topic
        choices = ["[0] Browse Tweets", "[1] Analyse Sentiment of Tweets", "[2] Get Top 10 Hashtags/Users", "[3] Get followers of given twitter user", 
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


    def _setup_submenu1(self):
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

            # Browse Tweets
            if main_sel == 0:
                print("Here are first 10 Tweets: ", self.tweets_df[0:10])
                print("For all Tweets look at")
                time.sleep(5)
            
            # Analyse Sentiment of Tweets
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
                        self.sentimentanalysis.most_used_words()
                        print("file is in wordcloud/generated")
                        time.sleep(3)
                    elif submenu_1_sel == 'b' or submenu_1_sel == 3:
                        self.submenu_1_exit = True
                        print("back selected")
                        time.sleep(1)
                self.submenu_1_exit = False

            # Get Top 10 Hashtags/Users
            elif main_sel == 2:
                # submenu 2
                while not self.submenu_2_exit:
                    submenu_2_sel = self.submenu_2.show()
                    if submenu_2_sel == 0:
                        pass
                    elif submenu_2_sel == 1:
                        pass
                    elif submenu_1_sel == 'b' or submenu_1_sel == 2:
                        self.submenu_2_exit = True
                        print("back selected")
                        time.sleep(1)
                self.submenu_2_exit = False
            
            # [3] Get followers of given twitter user
            elif main_sel == 3:
                print("Enter a twitter user: ")
                time.sleep(5)

            # [4] obtain...
            elif main_sel == 4:
                print("Enter a twitter user: ")
            
            # [c] Get followers of given twitter user
            elif main_sel == 5 or main_sel == 'c':
                print("Current Topic is:", self.querystring)
                self.querystring = self.get_querystring_from_user()
                self._setup_main_menu() # setup main menu new, so that topic refreshes
                self.twitterclient_v2.get_tweets(self.querystring)
                self.twitterclient_v2.store_tweets_to_csv()
                self.sentimentanalysis = SentimentAnalysis(self.querystring)
                self.tweets_df = pd.read_csv(f'fetched/{self.querystring}/{self.querystring}.csv', lineterminator='\n')
                
            # [q] Quit
            elif main_sel == 6 or main_sel == 'q':
                self.main_menu_exit = True
                print("You quit!")

    def get_TwitterID_to_analyse(self):
        twitterid = int(input("Enter Tweet ID of the Tweet to analyse: "))
        # TODO: Eingabe überoprüfen obs TwitterID überhaupt gibt
        # und nutzer ermöglichen, twitter id oder index einzugeben
        return twitterid


    def get_querystring_from_user(self):
        #Input from the User
        choice = input("Enter your querystring: ")
        return choice

