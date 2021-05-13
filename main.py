import bing_search_function as fn
import pyautogui
import sys
import datetime


USER_CREDENTIALS_TXT = 'user_credentials.txt'


def start_message():
    """
    Launch message to start the program.

    Okay: Program will continue.
    Cancel: Close program.
    :return: None
    """
    text = 'Would you like to run Microsoft Bing Search Bot?'
    title = 'Microsoft Bing Search Bot'
    run_program = pyautogui.confirm(text=text, title=title, buttons=['OK', 'Cancel'])

    if run_program.upper() == 'CANCEL':
        sys.exit()


def finish_message():
    """
    Alert message when the program is done running.
    Finish time will be display.
    :return: None
    """
    time_raw = datetime.datetime.now()
    time = time_raw.strftime('%Y/%m/%d %I:%M %p')

    text = 'Bing Search Finished: {}'.format(time)
    title = 'Microsoft Bing Search Bot'
    pyautogui.alert(text=text, title=title, button='OK')


def user_information():
    """
    Get user information from .txt file.
    User information are separated by a comma and newline.

    Clean and store username and password in a list of lists.
    :return: list: [[username1, pw1], [username2, pw2], ..., [username_n, pw_n]]
    """
    global USER_CREDENTIALS_TXT

    # Get a list of user username and password from .txt file.
    user_info = fn.txt_file_to_list(USER_CREDENTIALS_TXT)
    user_info_clean = []

    for info in user_info:
        username_and_pw = info.split(',')
        username = username_and_pw[0].strip()
        password = username_and_pw[1].strip()

        user_info_clean.append([username, password])

    return user_info_clean


def main():
    """
    Main body of the program.
    What we want to do:
        1. Setup user credentials, so we can loop through each account
        2. Open web browser to Bing
        3. Login
        4. Loop through searches to earn points, max out the limit
        5. Logout
        6. Repeat the process at the start of the loop until all user account are satisfy
    :return: None
    """
    start_message()

    credentials = user_information()
    for username, password in credentials:
        fn.open_web_browser()

        user = fn.Bing(username, password)
        user.login()
        user.input_search()

        for i in range(35):
            user.top_input_search()

        user.logout()

    finish_message()


if __name__ == "__main__":
    main()

