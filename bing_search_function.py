import webbrowser
import requests
import pyautogui
import time
import random
import sys


URL = 'https://www.bing.com/'

# Search File
SEARCH_TXT = 'search_list.txt'

# Button Location
# Replace value base on (x, y) coordinate for your display resolution.
LOGIN_BTN = (0, 0)
TOP_SEARCHBAR_BTN = (0, 0)
USER_ACCOUNT_BTN = (0, 0)
LOGOUT_BTN = (0, 0)


class Bing:
    """
    Automation function for Bing
    """
    global LOGIN_BTN, LOGOUT_BTN
    global TOP_SEARCHBAR_BTN, USER_ACCOUNT_BTN

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._search_list = load_search_list()
        self._used_search_list = []

    def search(self):
        """
        Randomly select a word from our search_list and check if it hasn't been used yet
        with used_search_list.
        :return: string: A new search.
        """
        search_word = random.choice(self._search_list)

        if search_word in self._used_search_list:
            return self.search()
        else:
            self._used_search_list.append(search_word)
            return search_word

    def input_search(self):
        """
        Automation

        Type search word and hit enter.
        :return: None
        """
        time.sleep(3)
        pyautogui.typewrite(self.search(), interval=0.1)
        pyautogui.typewrite(['enter'])
        time.sleep(3)

    def top_input_search(self):
        """
        Automation

        Used after the first search is completed.

        Highlight the search bar (located on the top of the webpage).
        Erase previous search.
        Type out new search and hit enter.
        :return: None
        """
        # Clicking on the search bar
        pyautogui.moveTo(TOP_SEARCHBAR_BTN[0], TOP_SEARCHBAR_BTN[1], duration=0.2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)

        # Erasing the previous search
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.typewrite(['backspace'])
        time.sleep(1)

        # New search
        self.input_search()

    def login(self):
        """
        Automation

        Handle the login information.
        Enter username and password.
        :return: None
        """
        # Click on login button.
        pyautogui.moveTo(LOGIN_BTN[0], LOGIN_BTN[1], duration=0.2)
        pyautogui.click()
        time.sleep(5)

        # Enter username.
        pyautogui.typewrite(self._username, interval=0.1)
        pyautogui.typewrite(['enter'])
        time.sleep(5)

        # Enter password.
        pyautogui.typewrite(self._password, interval=0.1)
        pyautogui.typewrite(['enter'])
        time.sleep(6)

    def logout(self):
        """
        Automation

        Logout of user account and close webpage.
        :return: None
        """
        # Clicking on the user account so we can attempt to logout.
        pyautogui.moveTo(USER_ACCOUNT_BTN[0], USER_ACCOUNT_BTN[1], duration=0.2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)

        # Click on the sign out button.
        pyautogui.moveTo(LOGOUT_BTN[0], LOGOUT_BTN[1], duration=0.2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(5)

        # Hotkey to exit a web browser tab
        pyautogui.keyDown('ctrl')
        time.sleep(1)
        pyautogui.keyDown('w')
        time.sleep(1)

        pyautogui.keyUp('ctrl')
        time.sleep(1)
        pyautogui.keyUp('w')
        time.sleep(3)


def open_web_browser():
    """
    Check if bing webpage is responding.

    If request code=200 (bing is responding), open webpage to bing.
    Else close program.
    :return: webbrowser: bing
    """
    global URL

    # Check http requests
    response = requests.get(URL)
    check_response = response.status_code

    # If we can connect, lets have our web browser page open
    if check_response == 200:
        # Open the web browser to bing
        webbrowser.open_new(URL)
        time.sleep(6)

    # If not, then we quit the program
    else:
        print('Could not connect to {url}'.format(url=URL))
        sys.exit()


def load_search_list():
    """
    Read and transfer from .txt file into a list.
    :return: list: list of searches
    """
    global SEARCH_TXT

    file = open(SEARCH_TXT, "r")
    readlines_raw = file.readlines()
    file.close()
    
    readlines_clean = []
    for lines in readlines_raw:
        readlines_clean.append(lines.strip())

    return readlines_clean
  
