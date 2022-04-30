from matplotlib.colors import TwoSlopeNorm
from simple_term_menu import TerminalMenu
from src.auth import Client
import pandas as pd
import time

class Menu:

    def __init__(self):
        title = "========================Twitter Data Analysis====================="
        choices = ["[0] Get Tweets to your entered topic", "[1] Analyse Sentiment of Tweets", "[2] Get Top 10 Hashtags"]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.main_menu_exit = False

        main_menu = TerminalMenu(
            menu_entries = choices,
            title = title,
            menu_cursor = cursor,
            menu_cursor_style = cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

        twitterClient = Client()

        while not self.main_menu_exit:
            main_sel = main_menu.show()

            if main_sel == 0:
                twitterClient.get_tweets("computer")
                twitterClient.store_tweets_to_csv()
                df = pd.read_csv("result.csv")
                print(df[0:10])
                print("Option 0")
                time.sleep(5)
            elif main_sel == 1:
                print("Option 1")
            elif main_sel == 9:
                self.main_menu_exit = True
                print("You quit!")

