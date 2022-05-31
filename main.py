from src.menu import Menu


def main():

    # default topic: 'computer'
    default_querystring = "computer"
    # -----------------------------------------------------------------------
    # START MENU
    myMenu = Menu(default_querystring)
    myMenu.menu_selection_loop()


if __name__ == "__main__":
    main()
