
import os  # For terminal clearing
import time  # for delays
import sys  # For writing to terminal with effects
import gspread  # Google Sheet Data
from google.oauth2.service_account import Credentials  # Google Sheets Access
from consolemenu import *  # Menu Generation
from consolemenu.items import *  # Menu Item Generation
from prettytable import PrettyTable  # Table Display
from colorama import Fore, Back, Style, init  # Terminal Text Colours
import getch  # Capture and record Keypresses
import hashlib  # For Hashing Login Passwords of Users
import re  # For Checking password strength with Regular Expressions
import random  # For generating random passwords

# Imports below are for interacting with the 'Have I Been Pwned' API
import pyhibp
from pyhibp import pwnedpasswords as pw

# Imports below all deal with Password Encryption & Decryption
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Google Sheet Credentials
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Initialise current list of users Google Sheets
SHEET = GSPREAD_CLIENT.open('vault_guard_db')
user_data = SHEET.worksheet('users')
login_usernames = user_data.col_values(1)
login_passwords = user_data.col_values(2)

# Initialise global variables for password encryption
current_user = None
key_source = None


def clear_screen():
    '''
    Clears the screen for improved visual experience in terminal
    '''
    os.system("clear")


def typewr(text):
    '''
    This function types text to the terminal with a delay, creating a
    typewriter effect.
    '''
    text_arr = [char for char in text]
    for i in text_arr:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.03)


def reorder_list_ids():
    '''
    This function Reorders the IDs of the users database, after an item has
    been deleted. This is done to avoid future duplicated IDs.
    '''
    for i in range(1, len(current_user.col_values(1)[1:])+1):
        current_user.update_cell(i+1, 1, i)


def generate_password():
    '''
    Generates a strong random password for user
    '''
    while True:
        length = input(('\nPlease Enter Generated Password Length'
                        ' (minimum 8 characters): \n'))
        if not (length.isdigit()) or int(length) < 8:
            print(Back.RED + 'Please Enter a valid Length.' + Style.RESET_ALL)
        else:
            length = int(length)
            break

    # Strong passwords should include at least 1 of each in p1 - p4
    p1 = [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    p2 = [i for i in 'abcdefghijklmnopqrstuvwxyz']
    p3 = [i for i in '0123456789']
    p4 = [i for i in '!@#$%^&*()-_=[]|;:,.<>?/~`"']
    p5 = [p1, p2, p3, p4]

    while True:
        new_password = ''
        for i in range(length):
            item = random.choice(p5)
            new_password += random.choice(item)

        # Check if the generated password is indeed strong, if not: Repeat
        strong_pass = []
        strong_pass.append(len(new_password) >= 8)
        strong_pass.append(bool(re.search("[A-Z]", new_password)))
        strong_pass.append(bool(re.search("[a-z]", new_password)))
        strong_pass.append(bool(re.search("[0-9]", new_password)))
        strong_pass.append(bool(re.search(
                        r'[!@#$%^&*()\[\]\-=_\\|;:,.<>?/~`"]', new_password)))
        if all(strong_pass):
            break
        else:
            continue

    print('\nYour generated Password: ' + Fore.YELLOW + new_password
                                        + Style.RESET_ALL)
    print('\nPress any key to continue')
    key = getch.getch()
    return new_password


def view_vault_read_only():
    '''
    Displays vault before CRUD operations, with passwords masked.
    '''
    gsheet_ids = SHEET.worksheet(current_user.title).col_values(1)[1:]
    gsheet_services = SHEET.worksheet(current_user.title).col_values(2)[1:]
    gsheet_usernames = SHEET.worksheet(current_user.title).col_values(3)[1:]
    gsheet_passwords = SHEET.worksheet(current_user.title).col_values(4)[1:]
    hide_pass_display = []
    for password in gsheet_passwords:
        hide_pass_display.append('********')
    table = PrettyTable()
    table.add_column("Entry ID", gsheet_ids)
    table.add_column("Service", gsheet_services)
    table.add_column("Username", gsheet_usernames)
    table.add_column("Password", hide_pass_display)
    print(table)
    if len(gsheet_ids) == 0:
        print(Fore.YELLOW + '\nYour Vault is currently empty. '
                            'Please add your first item.\n' + Style.RESET_ALL)


def view_vault():
    '''
    Displays vault with the option to reveal passwords
    '''
    show = False
    gsheet_ids = SHEET.worksheet(current_user.title).col_values(1)[1:]
    gsheet_services = SHEET.worksheet(current_user.title).col_values(2)[1:]
    gsheet_usernames = SHEET.worksheet(current_user.title).col_values(3)[1:]
    gsheet_passwords = SHEET.worksheet(current_user.title).col_values(4)[1:]
    hide_pass_display = []
    show_pass_display = []

    # Decrypted passwords are temporarily stored in show_pass_display
    for password in gsheet_passwords:
        hide_pass_display.append('********')
        show_pass_display.append(decrypt_password(password))

    while True:
        clear_screen()
        table = PrettyTable()
        table.add_column("Entry ID", gsheet_ids)
        table.add_column("Service", gsheet_services)
        table.add_column("Username", gsheet_usernames)
        if show:
            table.add_column("Password", show_pass_display)
        else:
            table.add_column("Password", hide_pass_display)

        print(table)

        if len(gsheet_ids) == 0:
            print(Fore.YELLOW + '\nYour Vault is currently empty. '
                                'Please add your first item.\n'
                                + Style.RESET_ALL)
        print('\nPress ' + Fore.GREEN + 'Space Bar'
                         + Style.RESET_ALL + ' to show/hide passwords')
        print('Press ' + Fore.YELLOW + 'Enter'
                       + Style.RESET_ALL + ' to return to the main menu')

        # Give users the option to display passwords with Spacebar
        key = getch.getch()
        if key == '\n':
            break
        elif key == ' ':
            show = not show


def add_to_vault():
    '''
    Allows user to add new stored credentials to vault, includes optional
    strong password generator that the user may use.
    '''
    print('Your Current Vault:\n')
    view_vault_read_only()

    # Generates new ID of 1, if the user vault is empty
    try:
        add_id = str(int(SHEET.worksheet(current_user.title)
                         .col_values(1)[-1])+1)
    except ValueError:
        add_id = 1

    # The 'while True' loops below enforce strong data handling
    while True:
        add_service = input('\nPlease Enter New Service: \n')
        if not (re.findall(r"\w", add_service)):
            print(Back.RED + 'Please Enter a valid service name.'
                           + Style.RESET_ALL)
        else:
            break

    while True:
        add_username = input('\nPlease Enter New Username: \n')
        if not (re.findall(r"\w", add_username)):
            print(Back.RED + 'Please Enter a valid Username name.'
                           + Style.RESET_ALL)
            print(Fore.YELLOW + 'If no Username is needed, type "None"'
                              + Style.RESET_ALL)
        else:
            break

    while True:
        add_password = input('\nPlease Enter New Password or type '
                             '"generate" to have one generated: \n')
        if not (re.findall(r"\w", add_password)):
            print(Back.RED + 'Please Enter a valid Password.'
                           + Style.RESET_ALL)
        elif add_password.lower() == 'generate':
            add_password = generate_password()
            break
        else:
            break

    en_password = encrypt_password(add_password)
    current_user.append_row([add_id, add_service, add_username, en_password])
    print('\n' + Fore.GREEN + 'Your Updated Vault:' + Style.RESET_ALL + '\n')
    view_vault_read_only()
    print('\nPress any key to return to the main menu.')
    key = getch.getch()


def edit_vault_item():
    '''
    Allows user to edit existing credentials in vault. Includes optional strong
    password generator the user may use when editing items.
    '''
    gsheet_ids = SHEET.worksheet(current_user.title).col_values(1)[1:]
    print('Your Current Vault:\n')
    view_vault_read_only()

    # Send users back to the main menu if their vaults are empty
    if len(gsheet_ids) == 0:
        print('You cannot edit from an empty vault.')
        print('\nPress any key to return to the main menu.')
        key = getch.getch()
        return

    print('\n')

    # The 'while True' loops below enforce strong data handling
    while True:
        to_edit = input('Please Enter the ID (in digits) of the vault item'
                        ' you would like to edit: \n')
        if to_edit not in gsheet_ids:
            print(Back.RED + '\n          That is not a valid ID              '
                           + Style.RESET_ALL)
            print('            Press Enter to try again')
            print(' Or press any other key to return to the Main Menu\n')
            key = getch.getch()
            if key == '\n':
                continue
            else:
                return
        else:
            break

    # Ask User for new information with which to edit item
    while True:
        add_service = input('\nPlease Enter New Service: \n')
        if not (re.findall(r"\w", add_service)):
            print(Back.RED + 'Please Enter a valid service name.'
                           + Style.RESET_ALL)
        else:
            break

    while True:
        add_username = input('\nPlease Enter New Username: \n')
        if not (re.findall(r"\w", add_username)):
            print(Back.RED + 'Please Enter a valid Username name.'
                           + Style.RESET_ALL)
            print(Fore.YELLOW + 'If no Username is needed, type "None"'
                              + Style.RESET_ALL)
        else:
            break

    while True:
        add_password = input('\nPlease Enter New Password or type '
                             '"generate" to have one generated: \n')
        if not (re.findall(r"\w", add_password)):
            print(Back.RED + 'Please Enter a valid Password.'
                           + Style.RESET_ALL)
        elif add_password.lower() == 'generate':
            add_password = generate_password()
            break
        else:
            break

    # Update existing items in place on Google Sheet
    to_edit = int(to_edit)+1
    current_user.update_cell(to_edit, 2, add_service)
    current_user.update_cell(to_edit, 3, add_username)
    current_user.update_cell(to_edit, 4, encrypt_password(add_password))
    print('\nItem ' + Fore.GREEN + f'ID# {to_edit-1}' + Style.RESET_ALL
                    + ' Updated. Press any key to return to the main Menu')
    key = getch.getch()
    return


def delete_from_vault():
    '''
    Allows user to remove exsiting credential from vault. Requires confirmation
    before deletion. Updates Credential IDs (on Google Sheet database) after
    item deletion.
    '''
    gsheet_ids = SHEET.worksheet(current_user.title).col_values(1)[1:]
    print('Your Current Vault:\n')
    view_vault_read_only()

    # Send users back to the main menu if their vaults are empty
    if len(gsheet_ids) == 0:
        print('You cannot delete from an empty vault.')
        print('\nPress any key to return to the main menu.')
        key = getch.getch()
        return

    print('\n')

    # The 'while True' loop below enforce strong data handling
    while True:
        to_del = input('Please Enter the ID (in digits) of the vault item '
                       'you would like to delete: \n')
        if to_del not in gsheet_ids:
            print(Back.RED + '\n          That is not a valid ID              '
                           + Style.RESET_ALL)
            print('            Press Enter to try again')
            print(' Or press any other key to return to the Main Menu\n')
            key = getch.getch()
            if key == '\n':
                continue
            else:
                return
        else:
            break

    # Confirm deletion from user before proceeding
    x = int(to_del)
    row_to_del = SHEET.worksheet(current_user.title).get_all_values()[x]
    print('\n' + Back.RED + 'Are you sure you want to delete the following '
                            'item?' + Style.RESET_ALL)
    table = PrettyTable()
    table.field_names = ["Entry ID", "Service", "Username", "Password"]
    table.add_row([row_to_del[0], row_to_del[1], row_to_del[2],
                  decrypt_password(row_to_del[3])])
    print(table)
    print('\n' + Fore.RED + ' ** Press y to delete ** ' + Style.RESET_ALL)
    print('Press any other key to return to the main menu')
    key = getch.getch()

    # Delete item (row) from Google Sheet
    if key == 'y' or key == 'Y':
        SHEET.worksheet(current_user.title).delete_rows(int(to_del)+1)
        reorder_list_ids()
        print('\nItem Deleted. Press any key to return to the main Menu')
        key = getch.getch()
    else:
        return


def check_leaks():
    '''
    Check for password breaches using the free API from haveibeenpwned.com
    User Vault passwords are checked against the regularly updated database at
    haveibeenpwned.com
    '''
    # Send users back to the main menu if their vaults are empty
    gsheet_ids = SHEET.worksheet(current_user.title).col_values(1)[1:]
    if len(gsheet_ids) == 0:
        print('Your vault is currently empty so cannot be checked.')
        print('\nPress any key to return to the main menu.')
        key = getch.getch()
        return

    typewr('The list of passwords in your vault '
           'will now be checked against a \n')
    typewr('known list of compromised passwords on' + Fore.GREEN +
           ' https://haveibeenpwned.com/\n' + Style.RESET_ALL)
    time.sleep(1)
    typewr('\nFor this purpose, ' + Fore.YELLOW + 'encrypted ("hashed") '
           + Style.RESET_ALL +
           'versions of your passwords\n')
    typewr('are sent to haveibeenpwned.com for security purposes.\n')
    time.sleep(1)

    print('\nPress y to continue or any other key to return to the main menu')
    key = getch.getch()
    if key.lower() != 'y':
        return

    print('\n')
    test_data = (current_user.get_all_values()[1:])

    print('Now accessing data from haveibeenpwned.com | Please wait...')
    for i in range(59):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.05)
    print('\n')

    for i in range(len(test_data)):
        d_pass = decrypt_password(test_data[i][3])
        del test_data[i][3]
        test_data[i].append(d_pass)

    table = PrettyTable()
    table.field_names = ["Entry ID", "Service", "Username", "Password",
                         "Data Breaches"]

    # The pyhibp library simplifies the API call to haveibeenpwned.com
    pyhibp.set_user_agent(ua="VaultGuard v1.0 (Code Institute Test Project)")

    any_passwords_breached = False

    for i in range(len(test_data)):
        breached = pw.is_password_breached(password=test_data[i][3])
        if breached:
            any_passwords_breached = True
            test_data[i].append(breached)
            table.add_row(test_data[i])

    '''
    Notify users of breached passwords, displaying passwords + number
    of data breaches in which the password was revealed. Otherwise
    confirm that no passwords have been revealed.
    '''
    if any_passwords_breached:
        print('\nThe following passwords were found to be compromised\n')
        print(table)
        print('\n' + Back.RED + 'Consider changing these passwords as '
                                'soon as possible' + Style.RESET_ALL + '\n')
    else:
        print(Fore.GREEN + 'Congratulations, no compromised passwords '
                           'were found.' + Style.RESET_ALL)

    print('Press any key to return to the main menu')
    key = getch.getch()


def display_login_menu():
    '''
    Displays menu for logged in users
    '''
    title = f"Welcome {current_user.title.capitalize()}"
    subtitle = " * Please select an option. *"
    menu = ConsoleMenu(title, subtitle)
    item1 = FunctionItem("Show Saved Passwords", view_vault)
    item2 = FunctionItem("Add a New Password", add_to_vault)
    item3 = FunctionItem("Edit a Vault Item", edit_vault_item)
    item4 = FunctionItem("Delete a Vault Item", delete_from_vault)
    item5 = FunctionItem("Check for exposed Passwords", check_leaks)

    menu.append_item(item1)
    menu.append_item(item2)
    menu.append_item(item3)
    menu.append_item(item4)
    menu.append_item(item5)

    return menu.show()


def encrypt_password(p):
    '''
    Uses SHA256 algorith to encrypt user passwords before writing them to the
    Google Sheet database. This function uses the built in
    Python Cryptography library. 'key_source' is tied to the user master
    password during account creation or login, and stays that way for the
    remainder of the session.
    '''
    salt = bytes(key_source.encode('utf-8'))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(
                                                key_source.encode('utf-8'))))
    FKEY = Fernet(key)
    # ** Encrypt and return password using Fernet Key **
    return FKEY.encrypt(p.encode()).decode()


def decrypt_password(p):
    '''
    Uses SHA256 algorith to decrypt user passwords from the Google Sheet
    database to display them in plaintext within the app. This function
    uses the built in Python Cryptography library.
    '''
    salt = bytes(key_source.encode('utf-8'))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(
                                                key_source.encode('utf-8'))))
    FKEY = Fernet(key)
    # ** Decrypt and return password using Fernet Key **
    return FKEY.decrypt(p).decode()


def correct_password(user_id, user_password):
    '''
    Used during login, this function compares a hash of the user entered
    password, against the hash of the previously saved password on Google
    Sheets.
    '''
    up_en = hashlib.sha256(bytes(user_password.encode('utf-8'))).hexdigest()
    return (up_en == login_passwords[user_id])


def login():
    '''
    Allows user to login, by comparing username and password to stored
    information on Google Sheet Database.
    '''
    while True:
        clear_screen()

        user_name = input("Please enter your username: \n")
        # Data Handling for incorrect username
        if user_name == '' or user_name == ' ' or len(user_name) < 3:
            print('\n')
            print(Back.RED + 'You entered an invalid username,'
                             ' please try again' + Style.RESET_ALL)
            print('         Press any key to try again')
            key = getch.getch()
            continue
        # Data Handling for absent username
        elif user_name not in login_usernames:
            print('\n')
            print(Back.RED + ' Username not found. Do you have an account? '
                           + Style.RESET_ALL)
            print('            Press Enter to try again')
            print(' Or press any other key to return to the Main Menu')
            key = getch.getch()
            if key == '\n':
                continue
            else:
                return

        elif user_name in login_usernames:
            for num, item in enumerate(login_usernames):
                if user_name == item:
                    user_id = num
            user_password = ''
            print("\nPlease Enter your password...")
            while True:
                key = getch.getch()
                if key == '\n':
                    break
                sys.stdout.write('*')
                sys.stdout.flush()
                user_password += str(key)
            if correct_password(user_id, user_password):
                global current_user
                global key_source
                key_source = user_password
                current_user = SHEET.worksheet(user_name)
                display_login_menu()
                break
            else:
                print('\n')
                print(Back.RED + ' Password Incorrect. Passwords are '
                                 'case-sensitive ' + Style.RESET_ALL)
            print('            Press Enter to try again')
            print(' Or press any other key to return to the Main Menu')
            key = getch.getch()
            if key == '\n':
                continue
            else:
                return


def strong_password(password, password2):
    '''
    Check the strength of a new user's password and displays password
    info allowing user to make corrections if a password is too weak.
    '''
    # 1: Length
    # 2: Uppercase
    # 3: Lowercase
    # 4: Number
    # 5: Special Character
    # 6: Match

    strong_pass = []
    strong_pass.append(len(password) >= 8)
    strong_pass.append(bool(re.search("[A-Z]", password)))
    strong_pass.append(bool(re.search("[a-z]", password)))
    strong_pass.append(bool(re.search("[0-9]", password)))
    strong_pass.append(bool(re.search(
                            r'[!@#$%^&*()\[\]\-=_\\|;:,.<>?/~`"]', password)))
    strong_pass.append(password == password2)

    # Write out Password Characteristics
    if all(strong_pass):
        typewr('\n' + Back.GREEN + ' PASSWORD IS STRONG '
                                 + Style.RESET_ALL + '\n')
    else:
        typewr('\n' + Back.RED + ' PASSWORD IS TOO WEAK '
                               + Style.RESET_ALL + '\n')

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
        print(Back.GREEN + ' The Passwords you entered match \n'
                         + Style.RESET_ALL)
    else:
        print(Back.RED + ' The Passwords you entered do not match \n'
                       + Style.RESET_ALL)

    return strong_pass


def create_new_account():
    '''
    Allows user to create a new account. Checks for valid username and strong
    password. If successfull, user credentials are stored in the Google Sheet
    Database (with the user password being hashed for future comparison).
    A new user database is then openened (a new Google Sheet Worksheet)
    to store user items. This function has strong input handling.
    '''
    global SHEET
    global user_data
    global login_usernames
    global login_passwords
    typewr('For creating an account with VaultGuard you need to create\n')
    typewr('a new ' + Fore.GREEN + 'USERNAME' + Style.RESET_ALL + ' and a new '
                    + Fore.RED + 'MASTER PASSWORD\n' + Style.RESET_ALL)
    time.sleep(1)
    typewr('\nThe ' + Fore.GREEN + 'USERNAME' + Style.RESET_ALL +
           ' can be anything you choose,\n')
    typewr('but needs to be at least 3 characters long.\n')
    time.sleep(1)
    typewr('\nThe ' + Fore.RED + 'MASTER PASSWORD' + Style.RESET_ALL +
           ' is very important:\n')
    typewr('This will be the password with which\n')
    typewr('your stored information is kept safe.\n')
    time.sleep(1)
    typewr('\n' + Back.RED + 'Create a STRONG password that you '
                             'will remember.\n' + Style.RESET_ALL)
    time.sleep(1)
    print('\nInclude upper and lowercase letters, digits, special, characters')
    print('(such as "!" or "@"), and make it at least 8 characters long.\n')

    # Ensure that usernames are valid, not in database, and not reserved word
    while True:
        new_username = input('Please enter your new username:\n')
        print('\n')
        if new_username in login_usernames:
            print('\n' + Back.RED + '     That username already exists      '
                                  + Style.RESET_ALL)
            print(Fore.YELLOW + ' Please log into your existing account \n')
            print(Style.RESET_ALL+'Press any key to return to the Main Menu\n')
            getch.getch()
            return
        if not (re.findall(r"\w", new_username)) or len(new_username) < 3:
            print(Back.RED + 'You entered an invalid username, '
                             'please try again' + Style.RESET_ALL)
            print('         Press any key to try again\n')
            key = getch.getch()
            continue
        if new_username.lower() == 'users':
            print(Back.RED + 'You cannot use the word "users" for '
                             'a username' + Style.RESET_ALL)
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
                time.sleep(0.1)

            # Update Database with new User Login Data & new worksheet
            new_password_encoded = hashlib.sha256(bytes(
                                    new_password.encode('utf-8'))).hexdigest()
            user_data.append_row([new_username, new_password_encoded])
            SHEET.add_worksheet(title=new_username, rows=1000, cols=4)
            SHEET.worksheet(new_username).append_row(['id',
                                                      'service',
                                                      'username',
                                                      'password'])

            # Close and reopen Google Sheet to ensure newest data available
            SHEET.client.session.close()
            SHEET = GSPREAD_CLIENT.open('vault_guard_db')
            user_data = SHEET.worksheet('users')
            login_usernames = user_data.col_values(1)
            login_passwords = user_data.col_values(2)

            print('\n\nAccount Created. You are now logged in.')
            typewr('\nPress any key to continue...')
            key = getch.getch()
            global current_user
            global key_source
            key_source = new_password
            current_user = SHEET.worksheet(new_username)
            display_login_menu()
            break

        else:
            print('       PLEASE ENTER A NEW STRONG PASSWORD')
            print('            Press Enter to try again')
            print(' Or press any other key to return to the Main Menu')
            key = getch.getch()
            if key == '\n':
                clear_screen()
                continue
            else:
                return


def display_main_menu():
    '''
    Welcome screen to greet users upon app opening.
    '''
    # Loads ASCII Art Logo to display in main menu.
    f = open('banner.txt', 'r')
    lines = f.read()
    f.close()

    title = lines
    subtitle = " * Secure Your World, One Password at a Time. *"
    menu = ConsoleMenu(title, subtitle)
    login_item = FunctionItem("Existing User: Login", login)
    create_account_item = FunctionItem("New User: Create Account",
                                       create_new_account)
    menu.append_item(login_item)
    menu.append_item(create_account_item)
    return menu.show()


clear_screen()
display_main_menu()
