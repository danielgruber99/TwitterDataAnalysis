from matplotlib.colors import TwoSlopeNorm
from simple_term_menu import TerminalMenu
from src.auth import Client
import pandas as pd
import time
import threading

from src.sentimentanalysis import SentimentAnalysis

class Menu:
    """
    This class handles the menu and provides to user a simple user interface in the command line. (Implemented with simple_term_menu)
    """
    def __init__(self, TwitterClient):
        # main menu
        self.main_menu_exit = False
        self.main_menu = None
        # submenu1
        self.submenu_1_exit = False
        self.submenu_1 = None
        # Client, qerystring and startmenu
        self.twitterclient = TwitterClient
        self.querystring = "computer" #default
        # start menu after setup
        self._setup_submenu1()
        self._setup_main_menu()
        self._menu_selection_loop()


    def _setup_main_menu(self):
        title = "=============================Twitter Data Analysis=========================="
        choices = ["[0] Get Tweets to your entered topic", "[1] Analyse Sentiment of Tweets", "[2] Get Top 10 Hashtags", "[q] Quit"]
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
        choices = ["[0] Analyse all tweets and get avg Polarity", "[1] Only analyse all tweets", "[2] Analyse single tweet", "[3] Get most used words.", "[b] Back."]
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
    
    def _setup_submenu1(self):
        title="========================Submenu 01: sentimentanalysis====================="
        choices = ["[0] Analyse all tweets and get avg Polarity", "[1] Only analyse all tweets", "[2] Analyse single tweet", "[3] Get most used words.", "[b] Back."]
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


    def _menu_selection_loop(self):
        # for default case
        self.twitterclient.get_tweets(self.querystring)
        self.twitterclient.store_tweets_to_csv()
        df = pd.read_csv(f'fetched/{self.querystring}/{self.querystring}.csv')
        
        while not self.main_menu_exit:
            main_sel = self.main_menu.show()

            if main_sel == 0:
                self.get_querystring_from_user()
                self.twitterclient.get_tweets(self.querystring)
                self.twitterclient.store_tweets_to_csv()
                df = pd.read_csv(f'fetched/{self.querystring}/{self.querystring}.csv')
                print("Here are first 10 Tweets: ", df[0:10])
                print("Fore all Tweets look at")
                time.sleep(5)
            elif main_sel == 1:
                sa = SentimentAnalysis(self.querystring)
                while not self.submenu_1_exit:
                    submenu_1_sel = self.submenu_1.show()
                    if submenu_1_sel == 0:
                        sa.analyse_all_tweets()
                        time.sleep(5)
                    elif submenu_1_sel == 1:
                        pass
                    elif submenu_1_sel == 2:
                        pass
                    elif submenu_1_sel == 3:
                        pass
                        sa.most_used_words()
                        time.sleep(3)
                    elif submenu_1_sel == 'b' or submenu_1_sel == 4:
                        self.submenu_1_exit = True
                        print("back selected")
                        time.sleep(1)

                self.submenu_1_exit = False
            elif main_sel == 3 or main_sel == 'q':
                self.main_menu_exit = True
                print("You quit!")


    def get_querystring_from_user(self):
        #Input from the User

        choice = input("Enter your querystring: ")

        self.querystring = choice
        return choice

