"""
Menu module for handling the entire user menu including main menu and all submenus.
"""
from simple_term_menu import TerminalMenu
import pandas as pd
import time
from src.sentimentanalysis import SentimentAnalysis
from src.dataprocessing import DataProcessing
import src.constants as c
import os
import sys
import shutil


class Menu:
    """
    This class handles the menu and provides to user a simple user interface in the command line (implemented with simple_term_menu).

    Parameters
    ----------
    default_querystring : str
        The querystring to start the program for.

    Attributes
    ----------
    querystring : str
    data : DataProcessing
    sentimentanalysis : SentimentAnalysis
    """

    def __init__(self, default_querystring):
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
        self.querystring = default_querystring  # default querystring
        self.data = DataProcessing(self.querystring)
        self.sentimentanalysis = SentimentAnalysis(self.data.get_tweets_text())
        # setup main_menu and all submenus
        self._setup_submenu0()
        self._setup_submenu1()
        self._setup_submenu2()
        self._setup_submenu4()
        self._setup_main_menu()
        # setup width of command line for pd dataframes
        pd.set_option("display.max_colwidth", 130)
        pd.set_option("display.html.table_schema", True)

    def _setup_main_menu(self):
        """
        Main Menu.
        """
        header = "=============================Twitter Data Analysis=========================="
        topic = "Topic: " + self.data.querystring
        title = header + "\n" + topic
        choices = [
            "[0] Browse Tweets/Users",
            "[1] Analyse Sentiment of Tweets",
            "[2] Get Top 10 Hashtags/Users",
            "[3] Get followers of given twitter user",
            "[4] Obtain tweets and profiles of followers of given twitter user",
            "[c] change Topic",
            "[q] Quit",
        ]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.main_menu = TerminalMenu(
            menu_entries=choices,
            title=title,
            menu_cursor=cursor,
            menu_cursor_style=cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def _setup_submenu0(self):
        """
        Submenu 00 for browsing Tweets/Users.
        """
        title = "========================Submenu 00: Browse Tweets/Users====================="
        choices = ["[0] Browse Tweets.", "[1] Browse Users.", "[b] Back."]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_0 = TerminalMenu(
            menu_entries=choices,
            title=title,
            menu_cursor=cursor,
            menu_cursor_style=cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def _setup_submenu1(self):
        """
        Submenu 01 for Sentiment Analysis.
        """
        title = (
            "========================Submenu 01: sentimentanalysis====================="
        )
        choices = [
            "[0] Analyse all tweets",
            "[1] Get average polarity",
            "[2] Analyse single tweet",
            "[3] Get most used words.",
            "[b] Back.",
        ]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_1 = TerminalMenu(
            menu_entries=choices,
            title=title,
            menu_cursor=cursor,
            menu_cursor_style=cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def _setup_submenu2(self):
        """
        Submenu 02 for getting Top 10 Hashtags/Users.
        """
        title = "========================Submenu 02: Get Top 10 Hashtags/Users====================="
        choices = ["[0] Get Top 10 Hashtags", "[1] Get Top 10 Users", "[b] Back."]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_2 = TerminalMenu(
            menu_entries=choices,
            title=title,
            menu_cursor=cursor,
            menu_cursor_style=cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    # Submenu 03 for getting followers of given twitter user
    # for submenu3 there is no submenu of simple-term-menu needed, as it is implemented by just demanding a user id to enter and then getting the result.

    def _setup_submenu4(self):
        """
        Submenu 04 for obtaining tweets and profiles of followers.
        """
        title = "========================Submenu 04: Obtain Tweets & Profiles of Followers====================="
        choices = [
            "[0] Enter a user ID for fetching tweets and profiles of followers",
            "[1] Browse profiles of followers",
            "[2] Browse Tweets of Followers",
            "[b] Back.",
        ]
        cursor = "> "
        cursor_style = ("fg_red", "bold")
        self.submenu_4 = TerminalMenu(
            menu_entries=choices,
            title=title,
            menu_cursor=cursor,
            menu_cursor_style=cursor_style,
            cycle_cursor=True,
            clear_screen=True,
        )

    def menu_selection_loop(self):
        """
        Menu selection loop handles every user request. Main menu and all submenus are controlled within this loop.
        """
        # needed to make it possible to switch from option 3 to option 4 and get without typing again an user id profiles of followers and tweets of followers
        userid = None

        while not self.main_menu_exit:
            # main menu
            main_sel = self.main_menu.show()
            # [0] Browse Tweets/Users
            if main_sel == 0:
                while not self.submenu_0_exit:
                    submenu_0_sel = self.submenu_0.show()
                    # Browse Tweets
                    if submenu_0_sel == 0:
                        self.data.get_tweets_df()
                        if self.data.tweets_df is not None:
                            start_browse_tweets = 0
                            browse_tweets_exit = False
                            while not browse_tweets_exit:
                                print(
                                    f"Tweets {start_browse_tweets} to {start_browse_tweets+c.NR_ENTRIES_PAGE}\n",
                                    self.data.tweets_df[[c.tweet_id, c.tweet_text]][
                                        start_browse_tweets : start_browse_tweets
                                        + c.NR_ENTRIES_PAGE
                                    ],
                                )
                                browse_tweets_input = input(
                                    f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} tweets. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n"
                                )
                                if browse_tweets_input == "n":
                                    start_browse_tweets += c.NR_ENTRIES_PAGE
                                elif browse_tweets_input == "p":
                                    if start_browse_tweets - c.NR_ENTRIES_PAGE >= 0:
                                        start_browse_tweets -= c.NR_ENTRIES_PAGE
                                elif browse_tweets_input == "m":
                                    self.data.generate_tweets_df_md_file()
                                    input("Press enter to continue...")
                                elif browse_tweets_input == "b":
                                    browse_tweets_exit = True
                                else:
                                    print("Invalid input.")
                            browse_tweets_exit = False
                        else:
                            print("No data could be fetched.")
                            input("Press enter to continue...")
                    # Browse Users
                    elif submenu_0_sel == 1:
                        self.data.get_users_df()
                        if self.data.users_df is not None:
                            start_browse_users = 0
                            browse_users_exit = False
                            while not browse_users_exit:
                                print(
                                    f"Tweets {start_browse_users} to {start_browse_users+c.NR_ENTRIES_PAGE}\n",
                                    self.data.users_df[
                                        [c.user_id, c.user_name, c.user_username]
                                    ][
                                        start_browse_users : start_browse_users
                                        + c.NR_ENTRIES_PAGE
                                    ],
                                )
                                browse_users_input = input(
                                    f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} tweets. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n"
                                )
                                if browse_users_input == "n":
                                    start_browse_users += c.NR_ENTRIES_PAGE
                                elif browse_users_input == "p":
                                    if start_browse_users - c.NR_ENTRIES_PAGE >= 0:
                                        start_browse_users -= c.NR_ENTRIES_PAGE
                                elif browse_users_input == "m":
                                    self.data.generate_users_df_md_file()
                                    input("Press enter to continue...")
                                elif browse_users_input == "b":
                                    browse_users_exit = True
                                else:
                                    print("Invalid input.")
                            browse_users_exit = False
                        else:
                            print("No data could be fetched.")
                            input("Press enter to continue...")
                    elif submenu_0_sel == "b" or submenu_0_sel == 2:
                        self.submenu_0_exit = True
                self.submenu_0_exit = False
            # [1] Analyse Sentiment of Tweets
            elif main_sel == 1:
                if self.sentimentanalysis is not None:
                    # submenu 1
                    while not self.submenu_1_exit:
                        submenu_1_sel = self.submenu_1.show()
                        # analyse all tweets
                        if submenu_1_sel == 0:
                            self.data.get_tweets_df()
                            if self.data.tweets_df is not None:
                                if "polarity" not in self.data.tweets_df:
                                    polarity_list = (
                                        self.sentimentanalysis.analyse_all_tweets()
                                    )
                                    self.data.tweets_df["polarity"] = polarity_list
                                    # optional TODO: inline Bar of polarity: https://towardsdatascience.com/make-your-pandas-dataframe-output-report-ready-a9440f6045c6#:~:text=matplotlib.org-,In%2Dline%20Bar%20Chart,-This%20is%20another
                                start_browse_tweets_polarity = 0
                                browse_tweets_polarity_exit = False
                                while not browse_tweets_polarity_exit:
                                    print(
                                        f"Tweets {start_browse_tweets_polarity} to {start_browse_tweets_polarity+c.NR_ENTRIES_PAGE}\n",
                                        self.data.tweets_df[
                                            [c.tweet_id, c.tweet_text, "polarity"]
                                        ][
                                            start_browse_tweets_polarity : start_browse_tweets_polarity
                                            + c.NR_ENTRIES_PAGE
                                        ],
                                    )
                                    browse_tweets_input = input(
                                        f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} tweets. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n"
                                    )
                                    if browse_tweets_input == "n":
                                        start_browse_tweets_polarity += (
                                            c.NR_ENTRIES_PAGE
                                        )
                                    elif browse_tweets_input == "p":
                                        if (
                                            start_browse_tweets_polarity
                                            - c.NR_ENTRIES_PAGE
                                            >= 0
                                        ):
                                            start_browse_tweets_polarity -= (
                                                c.NR_ENTRIES_PAGE
                                            )
                                    elif browse_tweets_input == "m":
                                        self.data.generate_tweets_df_md_file()
                                        input("Press enter to continue...")
                                    elif browse_tweets_input == "b":
                                        browse_tweets_polarity_exit = True
                                    else:
                                        print("Invalid input.")
                                browse_tweets_polarity_exit = False
                            else:
                                print("No data could be fetched.")
                                input("Press enter to continue...")
                        # get average polarity
                        if submenu_1_sel == 1:
                            avg_polarity_dict = (
                                self.sentimentanalysis.get_avg_polarity()
                            )
                            print(
                                f"The average polarity of your topic '{self.data.querystring}' is: '{avg_polarity_dict['avg_polarity']}' -> '{avg_polarity_dict['avg_polarity_meaning']}'"
                            )
                            input("\nPress enter to continue...")
                        # analyse single tweet
                        elif submenu_1_sel == 2:
                            print(
                                self.data.tweets_df[[c.tweet_id, c.tweet_text]][
                                    0 : c.NR_ENTRIES_PAGE
                                ]
                            )
                            index = self.input_twitterid()
                            polarity_meaning = (
                                self.sentimentanalysis.analyse_single_tweet(index)
                            )
                            print(
                                "Your selected Tweet at index",
                                index,
                                "is",
                                polarity_meaning,
                            )
                            input("\nPress enter to continue...")
                        # get most used words (outputs wordcloud with official twitterlogo as mask)
                        elif submenu_1_sel == 3:
                            self.sentimentanalysis.get_most_used_words(self.querystring)
                            input("\nPress enter to continue...")
                        # back
                        elif submenu_1_sel == "b" or submenu_1_sel == 4:
                            self.submenu_1_exit = True
                else:
                    print(
                        "Sentimentanalysis couldn't be done because no tweets could be provided."
                    )
                    input("Press enter to continue...")
                    self.submenu_1_exit = True
                self.submenu_1_exit = False
            # [2] Get Top 10 Hashtags/Users
            elif main_sel == 2:
                # submenu 2
                while not self.submenu_2_exit:
                    submenu_2_sel = self.submenu_2.show()
                    # Get Top 10 Hashtags
                    if submenu_2_sel == 0:
                        top_10_hashtags = self.data.get_top_10_hashtags()
                        if top_10_hashtags:
                            print("Top 10 Hashtags based on frequency: ")
                            for i in range(10):
                                print(f"{i+1}.:", "#" + top_10_hashtags[i][0])
                        else:
                            print(
                                "Top 10 hashtags couldn't be found as tweets_df couldn't be loaded."
                            )
                        input("\nPress enter to continue...")
                    # Get Top 10 Users
                    elif submenu_2_sel == 1:
                        top_10_users = self.data.get_top_10_users()
                        if top_10_users:
                            top_10_users_usernames = []
                            for user in top_10_users:
                                username = self.data.twitterclient.lookup_user(user[0])
                                top_10_users_usernames.append(username)
                            print("Top 10 Users based on their number of tweets: ")
                            for i in range(10):
                                print(
                                    f"{i+1}.: {top_10_users_usernames[i]} ({top_10_users[i][0]}) with {top_10_users[i][1]} tweets."
                                )
                        else:
                            print(
                                "Top 10 users couldn't be found as users_df couldn't be loaded."
                            )
                        input("\nPress enter to continue...")
                    # back
                    elif submenu_2_sel == "b" or submenu_2_sel == 2:
                        self.submenu_2_exit = True
                        print("back selected")
                self.submenu_2_exit = False
            # [3] Get followers of given twitter user
            elif main_sel == 3:
                self.data.get_users_df()
                if self.data.users_df is not None:
                    print(self.data.users_df[0 : c.NR_ENTRIES_PAGE])
                    print("Enter a twitter user: ")
                    userid = self.input_userid()

                    if userid != -1:
                        self.data.get_followers_df(userid)
                    else:
                        print(
                            "Your input does not match any user in this dataset. Please enter a user available in this data set."
                        )
                    if self.data.followers_df is not None:
                        start_browse_followers = 0
                        browse_followers_exit = False
                        while not browse_followers_exit:
                            print(
                                f"Followers {start_browse_followers} to {start_browse_followers+c.NR_ENTRIES_PAGE}\n",
                                self.data.followers_df[
                                    [
                                        c.follower_id,
                                        c.follower_name,
                                        c.follower_username,
                                    ]
                                ][
                                    start_browse_followers : start_browse_followers
                                    + c.NR_ENTRIES_PAGE
                                ],
                            )
                            browse_followers_input = input(
                                f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} followers. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n"
                            )
                            if browse_followers_input == "n":
                                start_browse_followers += c.NR_ENTRIES_PAGE
                            elif browse_followers_input == "p":
                                if start_browse_followers - c.NR_ENTRIES_PAGE >= 0:
                                    start_browse_followers -= c.NR_ENTRIES_PAGE
                            elif browse_followers_input == "m":
                                self.data.generate_followers_df_md_file(userid)
                                input("Press enter to continue...")
                            elif browse_followers_input == "b":
                                browse_followers_exit = True
                            else:
                                print("Input not valid.")
                        browse_followers_exit = False
                    else:
                        print("No data could be fetched.")
                        input("Press enter to continue...")
                else:
                    print("No data could be fetched.")
                    input("Press enter to continue...")
            # [4] obtain tweets and profiles of followers of given twitter user
            elif main_sel == 4:
                self.data.get_users_df()
                if self.data.users_df is not None:
                    # submenu 4
                    while not self.submenu_4_exit:
                        submenu_4_sel = self.submenu_4.show()
                        # Enter a user ID for fetching tweets and profiles and followers
                        if submenu_4_sel == 0:
                            print(self.data.users_df[0 : c.NR_ENTRIES_PAGE])
                            print("Enter a twitter user: ")
                            userid = self.input_userid()
                            if userid == -1:
                                print(
                                    "Your input does not match any user in this dataset. Please enter a user available in this data set."
                                )
                                input("Press enter to continue...")
                            else:
                                self.data.get_followers_df(userid)
                        # Browse profiles of followers
                        elif submenu_4_sel == 1:
                            if userid is None:
                                print(
                                    "Please enter a user id first under option '[0]' of this submenu4"
                                )
                                input("Press enter to continue...")
                            elif userid != -1:
                                # following line done alread after entering user id under option 0 in this submenu 4
                                # followers_df = self.twitterclient.fetch_followers(userid)
                                if self.data.followers_df is not None:
                                    start_browse_followers_profiles = 0
                                    browse_followers_profiles_exit = False
                                    pd.set_option("display.max_colwidth", 23)
                                    while not browse_followers_profiles_exit:
                                        print(
                                            f"Followers {start_browse_followers_profiles} to {start_browse_followers_profiles+c.NR_ENTRIES_PAGE}\n",
                                            self.data.followers_df[
                                                [
                                                    c.follower_id,
                                                    c.follower_name,
                                                    c.follower_username,
                                                    c.follower_bio,
                                                    c.follower_location,
                                                    c.follower_url,
                                                    c.follower_created_at,
                                                    c.follower_following,
                                                    c.follower_followers,
                                                ]
                                            ][
                                                start_browse_followers_profiles : start_browse_followers_profiles
                                                + c.NR_ENTRIES_PAGE
                                            ],
                                        )
                                        browse_followers_profiles_input = input(
                                            f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} followers. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n"
                                        )
                                        if browse_followers_profiles_input == "n":
                                            start_browse_followers_profiles += (
                                                c.NR_ENTRIES_PAGE
                                            )
                                        elif browse_followers_profiles_input == "p":
                                            if (
                                                start_browse_followers_profiles
                                                - c.NR_ENTRIES_PAGE
                                                >= 0
                                            ):
                                                start_browse_followers_profiles -= (
                                                    c.NR_ENTRIES_PAGE
                                                )
                                        elif browse_followers_profiles_input == "m":
                                            self.data.generate_followers_df_md_file(
                                                userid
                                            )
                                            input("Press enter to continue...")
                                        elif browse_followers_profiles_input == "b":
                                            browse_followers_profiles_exit = True
                                        else:
                                            print("Input not valid.")
                                    browse_followers_profiles_exit = False
                                    pd.set_option("display.max_colwidth", 130)
                                else:
                                    print("No data could be fetched.")
                                    input("Press enter to continue...")
                            else:
                                print(
                                    "Your input does not match any user in this dataset. Please enter a user available in this data set."
                                )
                        # Browse tweets of followers
                        elif submenu_4_sel == 2:
                            if userid is None:
                                print(
                                    "Please enter a user id first under option '[0]' of this submenu4"
                                )
                                input("Press enter to continue...")
                            elif userid != -1:
                                self.data.get_followers_tweets_df(userid)
                                if self.data.followers_tweets_df is not None:
                                    start_browse_followers_tweets = 0
                                    browse_followers_tweets_exit = False
                                    while not browse_followers_tweets_exit:
                                        print(
                                            f"Follower Tweets {start_browse_followers_tweets} to {start_browse_followers_tweets + c.NR_ENTRIES_PAGE}\n",
                                            self.data.followers_tweets_df[
                                                [
                                                    c.follower_id,
                                                    c.follower_tweet_id,
                                                    c.follower_tweet_text,
                                                ]
                                            ][
                                                start_browse_followers_tweets : start_browse_followers_tweets
                                                + c.NR_ENTRIES_PAGE
                                            ],
                                        )
                                        browse_followers_tweets_input = input(
                                            f"\nPress 'n'/'p' to get next/previous {c.NR_ENTRIES_PAGE} followers. Press 'm' to generate a markdown file. Press 'b' to go back to the main menu.\n"
                                        )
                                        if browse_followers_tweets_input == "n":
                                            start_browse_followers_tweets += (
                                                c.NR_ENTRIES_PAGE
                                            )
                                        elif browse_followers_tweets_input == "p":
                                            if (
                                                start_browse_followers_tweets
                                                - c.NR_ENTRIES_PAGE
                                                >= 0
                                            ):
                                                start_browse_followers_tweets -= (
                                                    c.NR_ENTRIES_PAGE
                                                )
                                        elif browse_followers_tweets_input == "m":
                                            self.data.generate_followers_tweets_df_md_file(
                                                userid
                                            )
                                            input("Press enter to continue...")
                                        elif browse_followers_tweets_input == "b":
                                            browse_followers_tweets_exit = True
                                        else:
                                            print("Input not valid.")
                                    browse_followers_tweets_exit = False
                                else:
                                    print("No data could be fetched.")
                                    input("Press enter to continue...")
                            else:
                                print(
                                    "Please provide first a user to fetch followers for under option '[0]'"
                                )
                        # back
                        elif submenu_4_sel == "b" or submenu_4_sel == 3:
                            self.submenu_4_exit = True
                    self.submenu_4_exit = False
                else:
                    print("No data could be fetched.")
                    input("Press enter to continue...")
            # [c] change Topic
            elif main_sel == 5 or main_sel == "c":
                if self.data.twitterclient.client is None:
                    print(
                        "Be aware that the twitterclient is not set up because authentication failed or no Bearer Token was provided."
                    )
                    print("Only already fetched data can be provided.")
                print("Current Topic is:", self.querystring)
                querystring = self.input_querystring_from_user()
                if querystring:
                    self.querystring = querystring
                    # check if folder for this querystring already exists, if so there is probably already fetched data
                    if os.path.isdir(f"fetched/{self.querystring}"):
                        # ask the user whether to hold the existing data set or fetch new
                        while True:
                            hold_existing_data = input(
                                "This topic exists already. Do you want fetch again most recent tweets for this topic [y]/[n]: "
                            )
                            if hold_existing_data == "y":
                                self.remove_eventually_old_data(self.querystring)
                                break
                            elif hold_existing_data == "n":
                                break
                            else:
                                print("Please enter either 'y' or 'n'.")
                    # setup DataProcessing
                    self.data = DataProcessing(self.querystring)
                    # check if tweets could be fetched and tweets text could be obtained for setting up sentimentanalysis
                    tweets_text = self.data.get_tweets_text()
                    if tweets_text:
                        self.sentimentanalysis = SentimentAnalysis(tweets_text)
                    else:
                        self.sentimentanalysis = None
                    # setup main menu new, so that topic refreshes
                    self._setup_main_menu()
                else:
                    print("no new topic entered, old topic is used.")
            # [q] Quit
            elif main_sel == 6 or main_sel == "q":
                self.main_menu_exit = True
                print("You quit!")

    def remove_eventually_old_data(self, querystring):
        """
        this function is needed to clean up eventually existing old data of topic if it is entered again.

        Parameters
        ----------
        querystring : str
            The querystring to delete the folder for.
        """
        folder_to_delete = f"fetched/{querystring}/"
        if os.path.exists(folder_to_delete):
            shutil.rmtree(folder_to_delete)

    def input_twitterid(self) -> int:
        """
        Get user input for which Tweet ID selected.

        Returns
        -------
        tiwtterid: int
            Index of the twitterid, -1 if input of user does not exists in the tweets dataframe.
        """
        while True:
            try:
                twitterid = int(
                    input("Enter Tweet ID or Index of the Tweet to analyse: ")
                )
                break
            except ValueError:
                print(
                    "A ValueError occured. Please enter the Tweet ID or corresponding index."
                )

        if self.check_twitterid_exists(twitterid):
            twitterid_list = self.data.get_tweets_id()
            if twitterid in twitterid_list:
                return twitterid_list.index(twitterid)
            else:
                return twitterid
        else:
            return -1

    def input_userid(self) -> int:
        """
        Get user input for which user ID selected.

        Returns
        -------
        users: int
            User Id of selected user either via userid or index, -1 if input of user does not exists in the users dataframe.
        """
        while True:
            try:
                userid = int(input("Enter User ID: "))
                break
            except ValueError:
                print(
                    "A ValueError occured. Please enter the user ID or corresponding index."
                )

        if self.check_userid_exists(userid):
            if userid in self.data.get_user_ids_without_duplicates():
                return userid
            else:
                return self.data.users_df[c.user_id][userid]
        else:
            return -1

    def check_twitterid_exists(self, twitterid) -> bool:
        """
        check if entered twitterid exists either as the twitter id or the corresponding index.

        Parameters
        ----------
        twitterid : int
            The twitterid to check for.

        Returns
        -------
        bool: True if twitterid exists in tweets datframe, False if not.
        """
        tweets = self.data.get_tweets_id()
        if twitterid in tweets or twitterid < self.data.tweets_df.shape[0]:
            return True
        return False

    def check_userid_exists(self, userid) -> bool:
        """
        check if entered userid exists either as the twitter id or the corresponding index.

        Parameters
        ----------
        userid : int
            The twitterid to check for.

        Returns
        -------
        bool: True if userid exists in tweets datframe, False if not.
        """
        users = self.data.get_user_ids_without_duplicates()
        if userid in users or userid < self.data.users_df.shape[0]:
            return True
        return False

    def input_querystring_from_user(self) -> str:
        """
        Get the input for the querystring from the user.

        Returns
        -------
        choice : str
            The entered topic/querystring from the user.
        """
        choice = input("Enter your querystring (or 'enter' to abort): ")
        return choice
