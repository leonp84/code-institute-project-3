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
import hashlib # For Hashing Login Passwords of Users (for this app)
import re # For Checking password strength with Regular Expressions

os.system("clear")

# Google Sheet Credentials and SHEET Variable
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('vault_guard_db')

# Initialise Users Information from Google Sheets
user_data = SHEET.worksheet('users')
login_usernames = user_data.col_values(1)[1:]
login_passwords = user_data.col_values(2)[1:]


def clear_screen():
    os.system("clear")

def type(text):
    text_arr = [char for char in text]
    for i in text_arr:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.03)

def display_login_menu(user_name):
    title = f"Welcome {user_name}"
    subtitle = " * Please select an option. *"
    menu = ConsoleMenu(title, subtitle)
    view_vault = FunctionItem("Show Saved Passwords", None)
    add_to_vault = FunctionItem("Add a New Password", None)
    edit_vault_item = FunctionItem("Edit a Vault Item", None)
    delete_from_vault = FunctionItem("Delete a Vault Item", None)
    check_leaks = FunctionItem("Check for exposed Passwords", None)

    menu.append_item(view_vault)
    menu.append_item(add_to_vault)
    menu.append_item(edit_vault_item)
    menu.append_item(delete_from_vault)
    menu.append_item(check_leaks)

    return menu.show()

    
def correct_password(user_id, user_password):
    user_password_encoded = hashlib.sha256(bytes(user_password.encode('utf-8'))).hexdigest()
    return(user_password_encoded == login_passwords[user_id])


def login():


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
            for num,item in enumerate(login_usernames):
                if user_name == item:
                    user_id = num
            user_password = ''
            print('\n')
            print("Please Enter your password...")
            while True:
                key = getch.getch()
                if key == '\n':
                    break
                sys.stdout.write('*')
                sys.stdout.flush()
                user_password += str(key)
            if correct_password(user_id, user_password):
                display_login_menu(user_name)
                break
            else:
                print('\n')
                print(Back.RED + ' Password Incorrect. Passwords are case-sensitive ' 
                                                                    + Style.RESET_ALL)
                print('           Press any key to try again')
                print('   Or press Enter to return to the Main Menu')
                key = getch.getch()
                if key == '\n':
                    return
                else:
                    continue


def strong_password(password, password2):
    # 1: Length, 2: Uppercase, 3: Lowercase, 4: Number, 5: Special Character, 6: Match

    strong_pass = []
    strong_pass.append(len(password) >= 8)
    strong_pass.append(bool(re.search("[A-Z]", password)))
    strong_pass.append(bool(re.search("[a-z]", password)))
    strong_pass.append(bool(re.search("[0-9]", password)))
    strong_pass.append(bool(re.search(r'[!@#$%^&*()\[\]\-=_\\|;:,.<>?/~`"]', password)))
    strong_pass.append(password == password2)
    # Write out Password Characteristics

    if all(strong_pass):
        type('\n' + Back.GREEN + ' PASSWORD IS STRONG \n')
    else:
        type('\n' + Back.RED + ' PASSWORD IS TOO WEAK \n')

    time.sleep(2)

    if strong_pass[0]:
        print(Back.GREEN + '\n Password is at least 8 characters long ')
    else:
        print(Back.RED + '\n Password needs to be at least 8 characters long ')

    if strong_pass[1]:
        print(Back.GREEN + ' Password contains an uppercase letter ')
    else:
        print(Back.RED + ' Password does not contain an uppercase letter ')


    if strong_pass[2]:
        print(Back.GREEN + ' Password contains a lowercase letter ')
    else:
        print(Back.RED + ' Password does not contain a lowercase letter ')


    if strong_pass[3]:
        print(Back.GREEN + ' Password contains a digit ')
    else:
        print(Back.RED + ' Password does not contain a digit ')

    if strong_pass[4]:
        print(Back.GREEN + ' Password contains a special character ')
    else:
        print(Back.RED + ' Password does not contain a special character ')  
        print(Back.YELLOW + 'Please include any one of these:')
        print(Back.YELLOW + '!@#$%^&*()-_=[]|;:,.<>?/~`"')

    if strong_pass[5]:
        print(Back.GREEN + ' The Passwords you entered match \n' + Style.RESET_ALL)
    else:
        print(Back.RED + ' The Passwords you entered do not match \n' + Style.RESET_ALL)
    
    return strong_pass


def create_new_account():
    # type('For creating an account with VaultGuard you need to create\n')
    # type('a new ' + Fore.BLUE + 'USERNAME' + Style.RESET_ALL + ' and a new ' 
    #                         + Fore.RED + 'MASTER PASSWORD\n' + Style.RESET_ALL)
    # time.sleep(1)
    # type('\nThe '+ Fore.BLUE + 'USERNAME' + Style.RESET_ALL + ' can be anything you choose,\n')
    # type('but needs to be at least 3 characters long.\n')
    # time.sleep(1)
    # type('\nThe ' + Fore.RED + 'MASTER PASSWORD' + Style.RESET_ALL + ' is very important:\n')
    # type('This will be the password with which\n')
    # type('your stored information is kept safe.\n')
    # time.sleep(1)
    # type('\n' + Back.RED + 'Create a STRONG password that you will remember.\n' + Style.RESET_ALL)
    # time.sleep(1)
    print('\nInclude upper and lowercase letters, digits, special, characters')
    print('(such as "!" or "@"), and make it at least 8 characters long.\n')

    while True:
        new_username = input('Please enter your new username:\n')
        print('\n')
        if new_username in login_usernames:
            print('\n' + Back.RED + '     That username already exists      ' )
            print(Back.YELLOW + ' Please log into your existing account \n')
            print(Style.RESET_ALL + 'Press any key to return to the Main Menu\n')
            getch.getch()
            return
        if new_username == '' or new_username == ' ' or len(new_username) < 3:
            print(Back.RED + 'You entered an invalid username, please try again' 
                                                                + Style.RESET_ALL)
            print('         Press any key to try again\n')
            key = getch.getch()
            continue
        break
    
    while True:
        new_password = input('Please enter your new password:\n')
        print('\n')
        new_password2 = input('Please enter your new password again:\n')
        if all(strong_password(new_password, new_password2)):
            print('Credentials valid. Creating Account...')
            for i in range(38):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(0.2)
            print('\n\nAccount Created. You are now logged in.')
            type('\nPress any key to continue...')
            key = getch.getch()
            display_login_menu(new_username)
            break

        else:
            print('    PLEASE ENTER A NEW STRONG PASSWORD')
            print('        Press any key to try again')
            print(' Or press Enter to return to the Main Menu')
            key = getch.getch()
            if key == '\n':
                return
            else:
                clear_screen()
                continue

    return ''


def display_main_menu():
    f = open('banner.txt', 'r')
    lines = f.read()
    f.close()

    title = lines
    subtitle = " * Secure Your World, One Password at a Time. *"
    menu = ConsoleMenu(title, subtitle)
    login_item = FunctionItem("Existing User: Login", login)
    create_account_item = FunctionItem("New User: Create Account", create_new_account)
    menu.append_item(login_item)
    menu.append_item(create_account_item)
    return menu.show()
    

clear_screen()
display_main_menu()




