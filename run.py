##############################################################################
import gspread # Google Sheet Data
from google.oauth2.service_account import Credentials # Google Sheets Access
from pprint import pprint # Temp, for debugging
import os # For terminal clearing
from consolemenu import * # Menu Generation
from consolemenu.items import * # Menu Item Generation
from colorama import Fore, Back, Style, init # Terminal Text Colours
import time # for delays
import sys # For writing to terminal with effects
import getch # Capture and record Keypresses

os.system("clear")

# Google Sheet Credentials and SHEET Variable
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vault_guard_db')

def clear_screen():
    os.system("clear")

def login():
    # Initialise Users Information from Google Sheets
    user_data = SHEET.worksheet('users')
    login_usernames = user_data.col_values(1)[1:]
    login_passwords = user_data.col_values(2)[1:]
    pprint(login_usernames)
    pprint(login_passwords)

    while True:
        clear_screen()
        user_name = input("Please enter your username: \n")
        if user_name == '' or user_name == ' ' or len(user_name) < 3:
            print('\n')
            print(Back.RED + 'You entered an invalid username, please try again' 
                                                                + Style.RESET_ALL)
            print('         Press any key to try again')
            key = getch.getch()
            continue
        elif user_name not in login_usernames:
            print('\n')
            print(Back.RED + ' Username not found. Do you have an account? ' 
                                                                + Style.RESET_ALL)
            print('        Press any key to try again')
            print(' Or press Enter to return to the Main Menu')
            key = getch.getch()
            if key == '\n':
                return
            else:
                continue
        elif user_name in login_usernames:
            user_password = ''
            print("Please Enter your password...")
            # while True:
            #     key = getch.getch()
            #     if key == '\n':
            #         break
            #     sys.stdout.write('*')
            #     sys.stdout.flush()
            #     passw += str(key)
            # print('\n')
            # print(passw)

    print('You entered: ' + user_name)


    return ''

def display_main_menu():
    f = open('banner.txt', 'r')
    lines = f.read()
    f.close()

    title = lines
    subtitle = " * Secure Your World, One Password at a Time. *"
    menu = ConsoleMenu(title, subtitle)
    login_item = FunctionItem("Existing User: Login", login)
    create_account_item = FunctionItem("New User: Create Account", None)
    menu.append_item(login_item)
    menu.append_item(create_account_item)
    return menu.show()
    
clear_screen()
login()
# display_main_menu()




    # if user_name in login_usernames:
    #     print('\n' + Back.RED + '     That username already exists      ' )
    #     print(Back.YELLOW + ' Please log into your existing account \n')
    #     print(Style.RESET_ALL + 'Press any key to return to the Main Menu\n')
    #     getch.getch()
    #     return