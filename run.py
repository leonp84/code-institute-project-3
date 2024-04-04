##############################################################################
import gspread # Google Sheet Data
from google.oauth2.service_account import Credentials # Google Sheets Access
from pprint import pprint # Temp, for debugging
import os # For terminal clearing
from consolemenu import * # Menu Generation
from consolemenu.items import * # Menu Item Generation

# Google Sheet Credentials and SHEET Variable
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
# CREDS = Credentials.from_service_account_file('creds.json')
# SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open('vault_guard_db')

# data = SHEET.worksheet('test')

def clear_screen():
    os.system("clear")

def display_main_menu():

    f = open('banner.txt', 'r')
    lines = f.read()
    f.close()

    title = lines
    subtitle = " * Secure Your World, One Password at a Time. * "
    menu = ConsoleMenu(title, subtitle)
    login_item = FunctionItem("Existing User: Login", None)
    create_account_item = FunctionItem("New User: Create Account", None)
    menu.append_item(login_item)
    menu.append_item(create_account_item)
    return menu.show()
    
clear_screen()
display_main_menu()

