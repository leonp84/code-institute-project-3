# VaultGuard

Welcome to the Readme file for VaultGuard, a web based personal password manager built with Python.
![VaultGuard Device Mockups](readme-images/all-devices-black.webp)


**Link to Live Site: https://vault-guard-f006577d0925.herokuapp.com/**
<br>
<br>
*For testing the application, please use the following login details:*

Username: 	**test**

Password: 	**12345**
<br>
<br>

## Table of Contents

1. [Overview](#overview)
2. [UX](#ux)
    - [User Stories](#user-stories)
    - [Site Concept](#site-concept)
    - [Flowchart](#flowchart)
    - [Site Design](#site-design)
3. [Features](#features)
    - [Existing Features](#existing-features)
        - [Site Logo](#site-logo)
        - [Header](#header)
        - [Add New User Item](#add-new-user-item)
        - [Main List Display](#main-list-display)
        - [User Controls](#user-controls)
        - [Optional Information Box](#optional-information-box)
        - [Footer](#footer)
    - [Future Ideas](#future-ideas)
4. [Testing](#testing)
    - [Manual Testing](#manual-testing)
    - [Validator Testing](#validator-testing)
    - [Lighthouse Testing](#lighthouse-testing)
    - [Bugs](#bugs)
        - [Fixed](#fixed)
        - [Unfixed](#unfixed)
5. [Deployment](#deployment)
    - [Links](#links)
6. [Credits](#credits)
    - [Content](#content)
    - [Media](#media)

## Overview

VaultGuard is a web based personal password manager, that allows users to store a list of usernames and passwords to a variety of services that they use. Each new user created a personal account with a strong master password that is verified, before they can then process to create a ‘vault’ or list of username + password credentials that they would like to save.

Users can add, edit, remove, or view vault items. VaultGuard also provides functionality for checking whether stored passwords were leaked in any previous public data breaches.

**Please Note**:  Even though user master passwords are securely Hashed, and stored passwords are properly encrypted, credentials are not stored in a secure enough environment to satisfy the requirements for a commercially used password manager. Above all, since I am not professionally trained in cryptography is recommended that VaultGuard be used for demo purposes only, and that *users do not store actual sensitive information* in the application database.


## UX

### User Stories

The sentences below outline possible motivations of *potential users* visiting the site. Goals of myself as site administrator is also added.

#### User

> As a user, I want to be able to create an account and then store information that is only visible to those who have my master password.

> As a user, I want my stores information to be available whenever I log into the application.

> As a user, I want to be able to have passwords generator by an application that can ensure me that my passwords are strong enough for security purposes.

> As a user, I want to be able to check whether passwords I currently use are safe, or whether they have been involved in any public data breaches over the last years. Checking these each individually is too time consuming and unpleasant: I want this to be automated for me.

#### Site Administrator

> As the app administrator I would want users to be aware of the utility and effectiveness of password managers and consider making use of professional password management software.

>  As the app administrator I want to ensure that users are taught the value of online security and understand the basics of password management, and password strength. I want my application to incorporate these elements in an easy-to-understand manner.

> As the app administrator my aim is to captivate users' interest in any future (paid) features the app could possibly offer.

> In my role as the app administrator, I endeavour to develop a product that establishes my identity as a reliable site/app developer, one who prioritizes the welfare of users.

### Site Concept

A simple password manager that focuses on:

- Security

- Strong input validation

- Data hygiene

### Flowchart

The below flowchart shows the application functionality and the expected user experience when engaging with app’s different functions. The flowchart if not exhaustive, since many steps require small additional steps that are not clearly documented, as this would make the flowchart overtly complex. But it gives a good idea of the app’s layout and functions. The flowchart was created with [Lucid Chart](https://www.lucidchart.com/pages/)

![VaultGuard Site Flowchart]( readme-images/flowchart.webp)

### Site Design

Being a terminal project, VaultGuard has very little design due to the constraints of the terminal environment. However, the following three Python libraries brought some design elements into the mix:

-	[Console Menu](https://pypi.org/project/console-menu/) | A python library by Aegir Hall that simplifies the creation of visually appealing menu’s for app users to interact with. The library greatly simplified app navigation.

-	[Prettytable](https://pypi.org/project/prettytable/) | Since the password manager uses tables to list information, this python library by Luke Maurits fits perfectly into the design by creating visually appealing tables with which to display information.

-	[Colorama](https://pypi.org/project/colorama/) | A python library by Jonathan Hartley that introduces foreground and background colour to the terminal. This helped when wanting to draw the user’s attention to important information being printed.
<br>
<br>
*The three libraries, mentioned above, in action*
![Three Libraries in Action](readme-images/three-libraries.webp)

As a final touch of colour, I updated the console background with a vault image and centred the console for improved user experience.

![Vault Image Background](readme-images/vault-image.webp)


## Features

All app features were built with **robust input validation** and **strong data hygiene**. 

### Existing Features

#### Login Menu

Users are greeted with the app’s ASCII logo, slogan, and a main menu. Here users can either select to either login or create a new account. The Console Menu Python library automatically takes care of input validation in menu’s, refusing to accept incorrect inputs.
![VaultGuard Main Menu](readme-images/screenshot.webp)


#### Login Option

User can login by first entering their usernames. If the entered username is not found within the existing list of usernames, users are encouraged the create a new account. Else, users may enter their master passwords which are masked with asterisk characters while being typed. If the password in incorrect users may try again or return to the main menu. Stored passwords are hashed, so the application verifies the user’s identity be also hashing the entered password and checking that against the hash of the stored password.
![VaultGuard Login Menu](readme-images/consolemenu.webp)

#### Create New Account Option
Upon choosing the create account option users are first presented with information describing how account creation works. 

![Create new account Screenshot](readme-images/new-account.webp)

Usernames can be anything but must be at least three characters long (not three black spaces). If an entered username in found in the list of existing usernames, users are encouraged to use their existing accounts and log in. New users also cannot use the word ‘users’ as a username since this is reserved for internal app usage. When users create a new password, this is checked to satisfy all requirements of a strong password, and if not, details are printed out so the user knows what steps to take to satisfy the app’s input validation. Note: An exception was made for the test account where the password is simply ‘12345’. Here, password generation is not available since user’s need to enter a Master password they can (1) easily remember, (2) but is also a strong password.

![Weak Password Screenshot](readme-images/weak-password.webp)

If an account is created successfully, the password is hashed, stored in the database along with the new username, and a new blank database (i.e. Google Worksheet) is opened and prepared for the new user.


#### View Vault
Here user’s may view their list of currently stored credentials. Users also have the option to temporarily view their decrypted passwords using the space bar key. If the user vault is empty, this is also displayed.

![View Vault Option](readme-images/prettytable.webp)

#### Add Password

This function allows users to add new credentials to their vault. A new (1) service name – i.e. the name of the website, app, or other service whose credentials they are saving, (2) username and (3) password. Here usernames and passwords are not checked for validation (except that they cannot be empty or consist only of spaces. This is because user’s need to be able to enter the actual usernames, email addresses or passwords that they currently use. When entering credentials for a new service users may also choose the app’s option of having a strong password automatically generated.

![Add item to Vault Screenshot](readme-images/add-item.webp)


#### Delete Password

This function allows users to delete a single credential from their vault. The vault is displayed, and user’s identify which item to delete by entering the ID of the credential. Any other input is not accepted. When the user has selected the item, the item is again displayed, and user confirmation is requested before the item is deleted. After deletion, the IDs of the remaining passwords are reordered from 1 upwards, to avoid future duplicate ID’s.

![Delete Password Screenshot](readme-images/delete-item.webp)


#### Edit Vault Item

Users can edit an existing credential in place by again indicating the item to be editing by entering its ID in digits. No other inputs are accepting. Upon editing, users may again use the app’s built in strong password generator if needed.

![Edit Item Screenshot](readme-images/edit-item.webp)

#### Check Data Breaches 

Check Data Breaches – This, final function of the app checks all the password’s in the user’s vault against the list of known compromise passwords on https://haveibeenpwned.com/ (HIBP). The free HIBP API allows anyone to check their passwords (or hashed versions thereof) for security, and VaultGuard makes use of this functionality.

The process is first explained to the user and confirmation requested before proceeding. If breached or leaked passwords are found the user is informed. If not, the user is congratulated and reassured that his/her accounts are not compromised.

![Check Data Breaches Screenshot](readme-images/check-leaks.webp)

#### Encryption Details

VaultGuard stores a list of user’s credentials in a Google Sheets Database.
Passwords are encrypted with a Secure Hash Algorithm 2 [(SHA-256)](https://en.wikipedia.org/wiki/SHA-2)  that uses random data as additional input [(salt)](https://en.wikipedia.org/wiki/Salt_(cryptography)) tied to the users Master Password. User App passwords (i.e. the passwords users use to login to VaultGuard) are similarly Hashed with a SHA-256 algorithm.

### Future Ideas

1.	**Improve security**: As mentioned in the [start](#vaultguard) of this document, as I am not trained in cryptography, the app certainly needs an overview by a professional software developer with experience in cyber security, for suggestions o improving the safekeeping of stored information.

2.	**Front End**: With the back-end side of the password manager in place, it would be nice to also build a visually stylish front end around the theme of an actual bank vault. This would naturally make the app more accessible to a larger audience.

3.	**Notes and Images**: It would be nice to allow future user’s to also store notes and even media (images, sound clips, videos) in their vaults.

## Testing

### Manual Testing

**- Testing Header & Footer**
| What will be Tested? | Expected Outcome | Test Procedure | Result |
|--|--|--|--|
|Header User Controls|The Toggle Theme button updates the colour palette on the entire site|Click on the toggle theme button|<span style="color: green; font-weight:bold">Pass</span>|
|Header User Controls|The Sound Effect button enables and disables the app’s sound effect|Click on the sound effects button|<span style="color: green; font-weight:bold">Pass</span>|
|Header User Controls|The Info box button hides/displays the information box|Click on the Info box button|<span style="color: green; font-weight:bold">Pass</span>|
|Footer Link|The footer link opens the correct page in a new tab|Click on the Footer link|<span style="color: green; font-weight:bold">Pass</span>|

<br>

**- Testing To do List Data Input & Display**
| What will be Tested? | Expected Outcome | Test Procedure | Result |
|--|--|--|--|
|Adding New Items Input Field|Users cannot enter invalid text for new items|Enter invalid text: Blank spaces and tabs| <span style="color: green; font-weight:bold">Pass</span> |
|Adding New Items Input Field|Clicking the Priority box serves as input submit|Click the priority box with text present in input field| <span style="color: green; font-weight:bold">Pass</span> |
|Adding New Items Input Field|As per above, but not with invalid (or non-existing) text|Click the priority box without text present in input field| <span style="color: green; font-weight:bold">Pass</span> |
|Adding New Items Input Field|Pressing ‘Enter’ on new item text field serves as input submit|Press Enter in the text input field with valid text present| <span style="color: green; font-weight:bold">Pass</span> |
|Adding New Items Input Field|As per above, but not with invalid (or non-existing) text|Press Enter in the text input field without valid text present| <span style="color: green; font-weight:bold">Pass</span> |
|Adding New Items Input Field|Duplicate items are not allowed when adding new items|Enter Duplicate Item| <span style="color: green; font-weight:bold">Pass</span> |
|Editing Existing Items|Users cannot enter invalid text when editing items|Enter invalid text: Blank spaces and tabs| <span style="color: green; font-weight:bold">Pass</span> |
|Editing Existing Items|Duplicate items are not allowed when editing text of existing items|Enter Duplicate Item as new list text content| <span style="color: green; font-weight:bold">Pass</span> |
|Remove Item Button|Users can always remove items from list|Click on Remove Item Icon| <span style="color: green; font-weight:bold">Pass</span> |
|Check Items|Users are able to check items off their list|Click on Circle 'checkbox' to the left of item text| <span style="color: green; font-weight:bold">Pass</span> |
|User Controls|Clicking ‘All’ shows all list items|Click on the ‘All’ button| <span style="color: green; font-weight:bold">Pass</span> |
|User Controls|Clicking ‘Active’ only shows active list items|Click on the ‘Active’ button| <span style="color: green; font-weight:bold">Pass</span> |
|User Controls|Clicking ‘Done’ only shows completed list items|Click on the ‘Done’ button| <span style="color: green; font-weight:bold">Pass</span> |
|User Controls|Clicking ‘Clear’ allows users remove checked items from the list|Click on the ‘Clear’ button| <span style="color: green; font-weight:bold">Pass</span> |
|User Controls|Clicking ‘Sort List’ allowed users to sort the to do list with priority items at the top and checked items at the bottom|Click on ‘Sort List’| <span style="color: green; font-weight:bold">Pass</span> |
|User Controls|‘Sort List’ works when new items are added, items removed, checked, unchecked etc.|Click on ‘Sort List’| <span style="color: green; font-weight:bold">Pass</span> |
|Items Left Check|The “items left” text update only when (1) items are checked, or (2) new items are added.|Review "Items left" number when list is in different states| <span style="color: green; font-weight:bold">Pass</span> |


### Validator Testing

The PEP8 Python formatting [validator](https://pep8ci.herokuapp.com/) initially showed many errors (some detailed below) when it first scanned my Python code. I took time to correct every little detail, including reformatting lines that were too long, and the current version of the app shows no errors when the Python code is run through the validator.

![PEP8 Pyton Validator Check](readme-images/pep8-check.webp)

### Bugs

#### Fixed
-	The bug that took the longest time to fix had to do with password encryption. I discovered that when tying encryption to a master password, the Fernet function (which is part of the Python cryptography library) still used salt (see [Encryption Details](#encryption-details) above) which meant that a Fernet Key needed to be stored locally somewhere within the database to enable to users to decrypt passwords once they log out of the app, and back in. I couldn’t do this as the Gspread library used JSON to write to Google Sheets and JSON could now store salt (in bytes) to Google Sheet. I overcame this (after much research) by tying the salt generation also to the user Master Password. I’m sure there are better ways to do this, involving Key Management Systems, but these were beyond the scope of this project. As it stands users are able to encrypt and decrypt passwords only when their Master Passwords are initially entered correctly.

-	Users were able to enter three black spaces as a new username which was excepted. Since the input validation only checked for an input length >= 3, three black spaces were able to pass. I then added an extra validation which uses a regular expression to only allow new usernames that also contain a character.

-	The PEP8 validator initially showed a multitude of issues, mostly having to do with visual formatting. These were all fixed by removing trailing or missing white space, shortening lines to a maximum of 79 characters and adding a final blank line to the end of the file.

-	In the single instance where I used a `try … except` block, the PEP8 validator did not like the use of a bare `except:` statement. I updated this to `except KeyError:`

-	For validating new login password strength, I struggled to have the computer also check for a variety of special characters. With the regular expression statement, since so many of the special characters required escaping with the `\` key, this proved challenging. I finally managed with some help (see credit below).

-	When a new user created an account and a new user database (i.e. Google Worksheet) was created, this was initially not picked up by the program which led to errors when the user tried to access their newly created vault. This bug was fixed by first closing and then reopening the Google Sheet within Python, which forced the program to re-read the data within the entire sheet.

-	When a new user tried to add a first item to his/her vault, the code threw an error since no previous item ID numbers were available to use as reference. I overcome this bug by using a `try … except` block which allowed the program to create a new ID of `1` in case no other IDs were available.

-	When a user wanted to edit an existing credential within their vault, I initially had some trouble updating individual cells within the database, as opposed to replacing entire rows or columns. The official gspread library documentation helped me fix this bug.

-	Initially users were able to check their stored passwords for breaches even when their vault was empty, which of course let to an error. This was fixed by first checking whether vaults had items in them before proceeding, as was already the case with the delete and edit functions.


#### Unfixed

There are no unfixed bugs that I’m aware of.

## Deployment

These are the steps I followed to deploy the project to Heroku:
1.  I created an Heroku account and logged in.
2.	I clicked New and created a new app on the dashboard.
3.	I entered a unique name, selected the region (in my case, Europe), and clicked Create app.
4.	Within the created app, I selected the tab, Settings.
5.	At the Config Vars section, I clicked Reveal Config Vars.
6.	To use Google Sheets, I added a new config var with the key CREDS. For the value, I pasted the contents of the creds.json file that was previously created when setting up the Google Sheets API.
7.	I added another config var with the key PORT and set the value to 8000.
8.	Below the Config Vars section, I clicked Add buildpack. I selected Python and saved. Then I added another buildpack and selected node.js. It was important that the buildpacks were shown in this order.
9.	Back in the Integrated Development Environment, I created a list of requirements by typing pip3 freeze > requirements.txt into the terminal. (Note: In my specific case, the cryptography library was NOT added to the requirements.txt file when using freeze, so I manually entered cryptography into the requirements.txt file.)
10.	I now ensured that a working version of my code was committed and pushed to GitHub
11.	Now on Heroku again, I navigated to the Deploy tab.
12.	I selected GitHub as the deployment method and connected to GitHub.
13.	I searched for the repository name of the project and clicked connect.
14.	Optionally, I enabled automatic deploys to deploy each time new code was pushed to the repository.
15.	I then finally clicked Deploy Branch to deploy the project.


### Links

Deployed Website: https://vault-guard-f006577d0925.herokuapp.com/<br>
GitHub Repository: https://github.com/leonp84/code-institute-project-3/


## Credits

### Content

-	The getch library and documentation proved very helpful for capturing keypresses within the python terminal.

-	Menu generation was done with Console Menu.

-	For help with gspread, especially with updating individual cells: Xx

-	For help with basic cryptographic concepts, involving hashing and encrypting, the following resources were very helpful: (Xx

-	For the (very tricky) Regex statement to capture all special characters (lines Xx – Xx) I asked ChatGPT to help after inputting the exact special characters I needed to be checked.

-	Inspiration for the Typewriter function from my fellow Code Institute classmate Dibyanka

-	Other general inspiration from previous Code Institute projects by Xx and Xx

-	For help with getting a Favicon to work with Heroku deployment I looked at the work of the very talented Julia Wagner.

-	All other Python libraries used were credited and explained within the opening lines of the application codebase.


### Media

-	ASCII Banner Logo generated with https://patorjk.com/software/taag

-	Favicon image from Pexels

-	Background image from Xx
