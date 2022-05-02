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
        self.main_menu_exit = False
        self.twitterclient = TwitterClient
        self.main_menu = None
        self.querystring = "computer" #default
        # start menu after setup
        self._setup_main_menu()
        self._menu_selection_loop()


    def _setup_main_menu(self):
        title = "========================Twitter Data Analysis====================="
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


    def _menu_selection_loop(self):
        while not self.main_menu_exit:
            main_sel = self.main_menu.show()
            
            # for default case
            self.twitterclient.get_tweets(self.querystring)
            self.twitterclient.store_tweets_to_csv()
            df = pd.read_csv(f'fetched/{self.querystring}.csv')


            if main_sel == 0:
                self.get_querystring_from_user()
                self.twitterclient.get_tweets(self.querystring)
                self.twitterclient.store_tweets_to_csv()
                df = pd.read_csv(f'fetched/{self.querystring}.csv')
                print(df[0:10])
                print("Option 0")
                time.sleep(5)
            elif main_sel == 1:
                sa = SentimentAnalysis(f'{self.querystring}')
                sa.analyse_all_tweets()
                time.sleep(5)
                print("Option 1")
            elif main_sel == 3 or main_sel == 'q':
                self.main_menu_exit = True
                print("You quit!")


    def get_querystring_from_user(self):
        #Input from the User

        choice = input("Enter your querystring: ")

        self.querystring = choice
        return choice

