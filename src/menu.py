from matplotlib.colors import TwoSlopeNorm
from simple_term_menu import TerminalMenu
import pandas as pd
import time
import threading
import keyboard as kb

from src.sentimentanalysis import SentimentAnalysis
from src.dataprocessing import DataProcessing
import src.constants as c
from tabulate import tabulate


class Menu:
    """
    This class handles the menu and provides to user a simple user interface in the command line. (Implemented with simple_term_menu)
    """
    def __init__(self, twitterclient):
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
        # submenu3
        # not needed, as no submenu from simple-term-menu for this is needed
        # submenu4
        self.submenu_4_exit = False
        self.submenu_4 = None
        # Client, qerystring and startmenu
        self.twitterclient = twitterclient
        self.querystring = twitterclient.querystring
        self.dataprocessing = DataProcessing(self.querystring)
        self.sentimentanalysis = SentimentAnalysis(self.dataprocessing.get_tweets_text())
        # all four dataframes: tweets_df, users_df, followers_df and follower_tweets_df
        self.tweets_df = self.dataprocessing.read_csv_file_tweets()
        self.users_df = None
        self.followers_df = None
        self.follower_tweets_df = None
        # setup main_menu and all submenus
        self._setup_submenu0()
        self._setup_submenu1()
        self._setup_submenu2()
        self._setup_submenu4()
        self._setup_main_menu()
        # setup width of command line for pd dataframes
        pd.set_option('display.max_colwidth', 130)
        pd.set_option("display.html.table_schema", True)
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
        choices = ["[0] Browse Tweets.", "[1] Browse Users.", "[b] Back."]
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

    #TODO: https://towardsdatascience.com/make-your-pandas-dataframe-output-report-ready-a9440f6045c6#:~:text=matplotlib.org-,In%2Dline%20Bar%20Chart,-This%20is%20another
    # neben avg polarity, auch durch apgen drurch jeden tweet und die Polarity davon
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
    
    # Submenu 03 for getting followers of given twitter user
    # for submenu3 there is no submenu of simple-term-menu needed, as it is implemented by just demanding a user id to enter and then getting the result.

    def _setup_submenu4(self):
        """
        Submenu 04 for obtaining tweets and profiles of followers.
        """
        title="========================Submenu 04: Obtain Tweets & Profiles of Followers====================="
        choices = ["[0] Enter a user ID for fetching tweets and profiles of followers", "[1] Browse profiles of followers", "[2] Browse Tweets of Followers", "[b] Back."]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_4 = TerminalMenu(
            menu_entries = choices,
            title = title,
            menu_cursor = cursor,
            menu_cursor_style = cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def _menu_selection_loop(self):
        """
        menu selection loop handles every user request. Main menu and all submenus are controlled within this loop.
        """
        # needed to make it possible to switch from option 3 to option 4 and get without typing again an user id profiles of followers and tweets of followers
        userid = None

        while not self.main_menu_exit:
            # main menu
            main_sel = self.main_menu.show()

            # [0] Browse Tweets/Users
            # TODO: utilize keyboard library, alread imported above as kb
            if main_sel == 0:
                while not self.submenu_0_exit:
                    submenu_0_sel = self.submenu_0.show()
                    # Browse Tweets
                    if submenu_0_sel == 0:
                        start_browse_tweets = 0
                        browse_tweets_exit = False
                        while not browse_tweets_exit:
                            print(f"Tweets {start_browse_tweets} to {start_browse_tweets+c.NR_ENTRIES_PAGE}\n", self.tweets_df[[c.tweet_id, c.tweet_text]][start_browse_tweets:start_browse_tweets+c.NR_ENTRIES_PAGE])
                            other_input = input(f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} tweets. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n")
                            if other_input == 'n':
                                start_browse_tweets+=c.NR_ENTRIES_PAGE
                            elif other_input == 'p':
                                if start_browse_tweets-c.NR_ENTRIES_PAGE >=0:
                                    start_browse_tweets-=c.NR_ENTRIES_PAGE
                            elif other_input == 'm':
                                self.tweets_df.to_markdown(f"fetched/{self.querystring}/tweets_markdown.md")
                                print(f"Files are stored at fetched/{self.querystring}/")
                                input("Press enter to continue...")
                            elif other_input == 'b':
                                browse_tweets_exit = True
                            else:
                                print("Invalid input.")
                        browse_tweets_exit = False
                    # Browse Users
                    elif submenu_0_sel == 1:
                        self.users_df = self.twitterclient.fetch_users(self.dataprocessing.get_users_without_duplicates())
                        start_browse_users = 0
                        browse_users_exit = False
                        while not browse_users_exit:
                            print(f"Tweets {start_browse_users} to {start_browse_users+c.NR_ENTRIES_PAGE}\n", self.users_df[[c.user_id, c.user_name, c.user_username]][start_browse_users:start_browse_users+c.NR_ENTRIES_PAGE])
                            other_input = input(f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} tweets. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n")
                            if other_input == 'n':
                                start_browse_users+=c.NR_ENTRIES_PAGE
                            elif other_input == 'p':
                                if start_browse_users-c.NR_ENTRIES_PAGE >=0:
                                    start_browse_users-=c.NR_ENTRIES_PAGE
                            elif other_input == 'm':
                                self.tweets_df.to_markdown(f"fetched/{self.querystring}/users_markdown.md")
                                print(f"Files are stored at fetched/{self.querystring}/")
                                input("Press enter to continue...")
                            elif other_input == 'b':
                                browse_users_exit = True
                            else:
                                print("Invalid input.")
                        browse_users_exit = False
                    elif submenu_0_sel == 'b' or submenu_0_sel == 2:
                        self.submenu_0_exit = True
                self.submenu_0_exit = False
                    
            # [1] Analyse Sentiment of Tweets
            elif main_sel == 1:
                # submenu 1
                while not self.submenu_1_exit:
                    submenu_1_sel = self.submenu_1.show()
                    # get avg polarity
                    if submenu_1_sel == 0:
                        avg_polarity_dict = self.sentimentanalysis.get_avg_polarity()
                        print(f"The average polarity of your topic '{self.querystring}' is: '{avg_polarity_dict['avg_polarity']}' -> '{avg_polarity_dict['avg_polarity_meaning']}'")
                        input("\nPress enter to continue...")
                    # analyse single tweet
                    elif submenu_1_sel == 1:
                        print(self.tweets_df[[c.tweet_id, c.tweet_text]][0:c.NR_ENTRIES_PAGE])
                        index = self.input_twitterid()
                        polarity_meaning = self.sentimentanalysis.analyse_single_tweet(index)
                        print("Your selected Tweet at index", index, "is", polarity_meaning)
                        input("\nPress enter to continue...")
                    # get most used words (outputs wordcloud with official twitterlogo as mask)
                    elif submenu_1_sel == 2:
                        self.sentimentanalysis.get_most_used_words()
                        print("file is in wordcloud/generated")
                        input("\nPress enter to continue...")
                    # back
                    elif submenu_1_sel == 'b' or submenu_1_sel == 3:
                        self.submenu_1_exit = True
                self.submenu_1_exit = False

            # [2] Get Top 10 Hashtags/Users
            elif main_sel == 2:
                # submenu 2
                while not self.submenu_2_exit:
                    submenu_2_sel = self.submenu_2.show()
                    # Get Top 10 Hashtags
                    if submenu_2_sel == 0:
                        top_10_hashtags = self.dataprocessing.get_top_10_hashtags()
                        print("Top 10 Hashtags based on frequency: ")
                        for i in range(10):
                            print(f"{i+1}.:", "#"+top_10_hashtags[i][0])
                        input("\nPress enter to continue...")
                    # Get Top 10 Users
                    elif submenu_2_sel == 1:
                        top_10_users = self.dataprocessing.get_top_10_users()
                        top_10_users_usernames = []
                        for user in top_10_users:
                            top_10_users_usernames.append(self.twitterclient.lookup_user(user[0]))
                        print("Top 10 Users based on their number of tweets: ")
                        for i in range(10):
                            print(f"{i+1}.: {top_10_users_usernames[i]} ({top_10_users[i][0]})", "with", top_10_users[i][1], "tweets.")
                        input("\nPress enter to continue...")
                    # back
                    elif submenu_2_sel == 'b' or submenu_2_sel == 2:
                        self.submenu_2_exit = True
                        print("back selected")
                self.submenu_2_exit = False
            
            # [3] Get followers of given twitter user
            elif main_sel == 3:
                print(self.tweets_df[0:c.NR_ENTRIES_PAGE])
                print("Enter a twitter user: ")
                userid = self.input_userid()

                if userid != -1:
                    self.followers_df = self.twitterclient.fetch_followers(userid)
                else:
                    print("Your input does not match any user in this dataset. Please enter a user available in this data set.")
                start_browse_followers = 0
                browse_followers_exit = False
                while not browse_followers_exit:
                    print(f"Followers {start_browse_followers} to {start_browse_followers+c.NR_ENTRIES_PAGE}\n",self.followers_df[[c.follower_id, c.follower_name, c.follower_username]][start_browse_followers:start_browse_followers+c.NR_ENTRIES_PAGE])
                    browse_followers_input = input(f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} followers. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n")
                    if browse_followers_input == 'n':
                        start_browse_followers+=c.NR_ENTRIES_PAGE
                    elif browse_followers_input == 'p':
                        if start_browse_followers-c.NR_ENTRIES_PAGE >=0:
                            start_browse_followers-=c.NR_ENTRIES_PAGE
                    elif browse_followers_input == 'b':
                        browse_followers_exit = True
                    else:
                        print("Input not valid.")
                browse_followers_exit = False

            # [4] obtain tweets and profiles of followers of given twitter user
            elif main_sel == 4:
                # submenu 4
                while not self.submenu_4_exit:
                    submenu_4_sel = self.submenu_4.show()
                    # Enter a user ID for fetching tweets and profiles and followers
                    if submenu_4_sel == 0:
                        print(self.tweets_df[0:c.NR_ENTRIES_PAGE])
                        print("Enter a twitter user: ")
                        userid = self.input_userid()
                        # TODO: check if userid valid
                        if userid is None:
                            print("Please enter a user id first under option '[0]' of this submenu4")
                        elif userid == -1:
                            print("Your input does not match any user in this dataset. Please enter a user available in this data set.")
                        else:
                            self.followers_df = self.twitterclient.fetch_followers(userid)
                    # Browse profiles of followers
                    elif submenu_4_sel == 1:
                        if userid is None:
                            print("Please enter a user id first under option '[0]' of this submenu4")
                        elif userid != -1:
                            # following line done alread after entering user id under option 0 in this submenu 4
                            #followers_df = self.twitterclient.fetch_followers(userid)
                            start_browse_followers_profiles = 0
                            browse_followers_profiles_exit = False
                            while not browse_followers_profiles_exit:
                                print(f"Followers {start_browse_followers_profiles} to {start_browse_followers_profiles+c.NR_ENTRIES_PAGE}\n", self.followers_df[start_browse_followers_profiles:start_browse_followers_profiles+c.NR_ENTRIES_PAGE])
                                browse_followers_profiles_input = input(f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} followers. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n")
                                if browse_followers_profiles_input == 'n':
                                    start_browse_followers_profiles+=c.NR_ENTRIES_PAGE
                                elif browse_followers_profiles_input == 'p':
                                    if start_browse_followers_profiles-c.NR_ENTRIES_PAGE >= 0:
                                        start_browse_followers_profiles-=c.NR_ENTRIES_PAGE
                                elif browse_followers_profiles_input == 'b':
                                    browse_followers_profiles_exit = True
                                else:
                                    print("Input not valid.")
                            browse_followers_profiles_exit = False
                        else:
                            print("Your input does not match any user in this dataset. Please enter a user available in this data set.")
                    # Browse tweets of followers
                    elif submenu_4_sel == 2:
                        if self.followers_df is not None:
                            followerids = self.followers_df[c.user_id]
                            # fetch only tweets for the 50 first followers, otherwise it takes so long
                            self.follower_tweets_df = self.twitterclient.fetch_tweets_of_followers(followerids[0:50])
                            start_browse_followers_tweets = 0
                            browse_followers_tweets_exit = False
                            while not browse_followers_tweets_exit:
                                print(f"Follower Tweets {start_browse_followers_tweets} to {start_browse_followers_tweets + c.NR_ENTRIES_PAGE}\n", self.follower_tweets_df[start_browse_followers_tweets : start_browse_followers_tweets + c.NR_ENTRIES_PAGE])
                                browse_followers_tweets_input = input(f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} followers. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n")
                                if browse_followers_tweets_input == 'n':
                                    start_browse_followers_tweets+=c.NR_ENTRIES_PAGE
                                elif browse_followers_tweets_input == 'p':
                                    if start_browse_followers_tweets-c.NR_ENTRIES_PAGE >= 0:
                                        start_browse_followers_tweets-=c.NR_ENTRIES_PAGE
                                elif browse_followers_tweets_input == 'b':
                                    browse_followers_tweets_exit = True
                                else:
                                    print("Input not valid.")
                            browse_followers_tweets_exit = False
                        else:
                            print("Please provide first a user to fetch followers for under option '[0]'")
                    # back
                    elif submenu_4_sel == 'b' or submenu_4_sel == 3:
                        self.submenu_4_exit = True
                        print("back selected")
                        time.sleep(1)
                self.submenu_4_exit = False
                
            # [c] change Topic
            elif main_sel == 5 or main_sel == 'c':
                print("Current Topic is:", self.querystring)
                self.querystring = self.input_querystring_from_user()
                self._setup_main_menu() # setup main menu new, so that topic refreshes
                self.twitterclient.fetch_tweets(self.querystring)
                self.dataprocessing = DataProcessing(self.querystring)
                self.sentimentanalysis = SentimentAnalysis(self.dataprocessing.get_tweets_text())
                self.tweets_df = self.dataprocessing.read_csv_file_tweets()
                
            # [q] Quit
            elif main_sel == 6 or main_sel == 'q':
                self.main_menu_exit = True
                print("You quit!")

    def input_twitterid(self):
        """
        Get user input for which Tweet ID selected.
        """
        while True:
            try:
                twitterid = int(input("Enter Tweet ID or Index of the Tweet to analyse: "))
                break
            except ValueError:
                print('A ValueError occured. Please enter the Tweet ID or corresponding index.')

        if self.check_twitterid_exists(twitterid):
            return twitterid
        else:
            return -1

    def input_userid(self):
        """
        Get user input for which user ID selected.
        """
        while True:
            try:
                userid = int(input("Enter User ID: "))
                break
            except ValueError:
                print('A ValueError occured. Please enter the user ID or corresponding index.')

        if self.check_userid_exists(userid):
            if userid in self.dataprocessing.get_users_without_duplicates():
                return userid
            else:
                return self.tweets_df[c.user_id][userid]
        else:
            return -1

    def check_twitterid_exists(self, twitterid):
        """
        check if entered twitterid exists either as the twitter id or the corresponding index.
        """
        tweets = self.dataprocessing.get_tweets_id()
        if twitterid in tweets or twitterid < self.tweets_df.shape[0]:
            return True
        return False

    def check_userid_exists(self, userid):
        """
        check if entered userid exists either as the twitter id or the corresponding index.
        """
        users = self.dataprocessing.get_users_without_duplicates()
        if userid in users or userid < self.tweets_df.shape[0]:
            return True
        return False
    
    def input_querystring_from_user(self):
        """
        Get the input for the querystring from the user.
        """
        choice = input("Enter your querystring: ")
        return choice
