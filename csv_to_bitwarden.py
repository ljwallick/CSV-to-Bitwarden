"""Module Docstring"""

import csv
from os import get_terminal_size, system, name as osname
from difflib import get_close_matches
from uri_mapping import ANDROID_MAPPING, HREF_MAPPING

clr = ('clear', 'cls')[osname == 'nt']

bitwarden = ["folder", "favorite", "type", "name", "notes", "fields", "reprompt",\
             "login_uri", "login_username", "login_password", "login_totp"]
microsoft = {'login_uri': 'url', 'login_username': 'username', 'login_password': 'password'}

def main():
    """Main Program"""
    f = Folders(False)
    to_bitwarden = bitwarden.copy()
    with open('./Passwords.csv', 'r', encoding='utf-8') as f_read:
        with open('Bitwarden_Pswds.csv', 'w', encoding='utf-8') as f_write:
            pswd_writer = csv.writer(f_write, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            passreader = csv.reader(f_read)

            system(clr)
            express = input("Express Mode? Removes less important fields. (y/n): ")\
                .lower().startswith(('y'))

            for i, row in enumerate(passreader):
                if i == 0:
                    if row != ["url", "username", "password"]:
                        raise ValueError("Must be a Microsoft or Google csv file.")
                    pswd_writer.writerow(bitwarden)
                    to_bitwarden.clear()
                    continue

                name, capitalized = get_names(row[0])

                confirm = { f"{j+1})": f"{n if capitalized else n.title()}, "
                           for j, n in enumerate(name) }
                custom = f"{len(confirm) + 1}) Custom"

                while True:
                    system(clr)
                    print("Type 'skip' to skip an entry. Will not return to it.")

                    if row[0].startswith('android://'):
                        print('App: @' + row[0].rsplit('@', 1)[1].rstrip('/'), end='; ')
                    else:
                        if '://' in row[0]:
                            c = row[0].count('/')
                            print('Link: ' + row[0].rsplit('/', c-2)[0], end='; ')
                        else:
                            print('Link: ' + row[0].lstrip('/').split('/')[0], end='; ')

                    if row[1].find('@') >= 0:
                        print('Email:', row[1])
                    else:
                        print('Username:', row[1] or 'None')

                    name_num = input(f"{''.join(f"{k} {v}" for k, v in confirm.items())}{custom} ")
                    if name_num.lower() == 'skip':
                        continue
                    if not name_num.isdigit():
                        input("Must choose a number.\n")
                        continue
                    name_num = int(name_num)

                    if name_num == len(confirm) + 1:
                        new_name = input("Please enter custom name: ")
                        if not new_name.strip():
                            input("You must enter something!\n")
                            continue
                        if input(f"Name will be '{new_name}'. Confirm? (y/n) ") in ('y', ''):
                            break
                        continue
                    if 0 < name_num <= len(confirm):
                        new_name = confirm[f"{name_num})"].rstrip(', ')
                        break
                    else:
                        input("Please choose a number shown.\n")
                        continue
                if not row[1]:
                    row[1] = input('If you know Email/Username, please input: ').strip()

                folder = f.main()

                favorite, notes, reprompt, totp = '', '', '', ''

                if not express:
                    print('Press Enter to skip or deny any of the following:')
                    favorite = int( bool( input("Favorite? ") ) )
                    notes = input('Notes? ')
                    reprompt = int( bool( input('Require Bitwarden verification? ') ) )
                    totp = input('Do you have a TOTP key? ')

                to_bitwarden += [folder, favorite, 'login', new_name, notes,\
                                 '', reprompt, row[0], row[1], row[2], totp]

                pswd_writer.writerow(to_bitwarden)
                to_bitwarden.clear()

def get_names(row:str) -> tuple[list[str], bool]:
    """Gets the possible names from the link"""

    capitalized = False
    if row.startswith('android://'):
        name = row.rsplit('@', 1)[1].rstrip('/')
        app_names = ANDROID_MAPPING.get(name, None)
        if app_names:
            # If it is in the dictionary, then we know the name(s)
            name = app_names
            capitalized = True
        else:
            # Most apps use @com. or @tv.
            if name.startswith(('com', 'tv')):
                name = name.split('.', 1)[1]
            name = name.split('.')
    else:
        name = row.split('/')
        if name[0].startswith('http'):
            # ['https:', '', 'docs.google.com', '...']
            name = name[2]
        else:
            name = name[0]
        if name.startswith(('www', 'ww1')):
            name = name.split('.', 1)[1]

        web_names = None  # Initialize to fix the warning
        temp_name = name.split('.')

        # Try progressively shorter domains
        for i in range(len(temp_name)):
            current_domain = '.'.join(temp_name[i:])
            web_names = HREF_MAPPING.get(current_domain, None)
            if web_names:
                break  # Found a match!

            # Stop at domain.tld (don't go to just .com)
            if len(temp_name[i:]) <= 2:
                break

        if web_names:
            # If it is in the dictionary, then we know the names(s)
            name = web_names
            capitalized = True
        else:
            # If we couldn't find it, then we will make educated guesses
            # Just some popular domains we can cut off.
            if name.endswith(('com', 'co', 'edu', 'gov', 'net', 'org',\
                              'shop', 'site', 'store', 'tech', 'xyz')):
                name = name.rsplit('.', 1)[0]
            name = name.split('.')

    return (name, capitalized)

class Folders():
    """Class that holds all folders and functions for folder creation"""
    def __init__(self, do_main=True):
        # Predefined list of common categories
        self.folder_list = [
            "Personal", "Work", "Social Media", "Banking", "Shopping", 
            "Entertainment", "Gaming", "Email", "Streaming", "News",
            "Education", "Health", "Travel", "Utilities", "Government",
            "Insurance", "Finance", "Subscriptions", "Forums", 
            "Music", "Sports", "Photography", "Food", "Tech",
            "Cloud Storage", "Security", "VPN", "Messaging"
        ]
        self.size = get_terminal_size().columns
        if do_main:
            self.main()

    def main(self):
        """Basically the main body to create, view, and find folders"""

        while True:
            inp = input("Name a folder or type 'list folders' to view all.\n  > ")
            # See if they want to display folders
            if inp.lower() == 'list folders':
                self.list_folders()
                continue
            elif not inp:
                return ''
            # Not too long, now!
            if len(inp) > 25:
                print('Are you trying to rename a protein, titin? Please make a smaller name!')
                continue

            result = self.get_folder(inp)
            if result is not None:
                return result
            # If result is None, user declined to create folder, so loop again

    def new_folder(self, name):
        """Creates a new folder"""
        self.folder_list.append(name)

    def list_folders(self):
        """Lists the folders to see their names"""
        if not self.folder_list:
            print('There are no folders, you dum dum!')
            return
        if self.size <= 25:
            # 25 is the allowed length of a single term (which is long, still)
            print(*self.folder_list, sep=', ')
            return
        length = sum(len(n) for n in self.folder_list) + (len(self.folder_list)-1) * 2
        if length < self.size:
            print(*self.folder_list, sep='  ')
            return
        # How wide each term should be
        term_width = max(len(n) for n in self.folder_list)
        # How many terms can fit on each line
        terms_wide = self.size // (term_width + 2*(len(self.folder_list)!=1) )

        terms = list(map(lambda x: x + ' ' * (term_width - len(x)), self.folder_list))

        for line_start in range(0, len(self.folder_list), terms_wide):
            print('  '.join(terms[line_start:line_start + terms_wide]))

    def get_folder(self, folder):
        """Gets the folder to be used"""

        does_exist = self.check_existance(folder)
        if does_exist:
            # It will be the correct name.
            return does_exist
        else:
            confirm = input('Folder does not exist. Make a new one? (y/n) ')
            if confirm in ('y', ''):
                self.new_folder(folder)
                return folder
            else:
                return None  # Signal to main() to ask again

    def check_existance(self, name):
        """Checks if a folder already exists"""
        if name in self.folder_list:
            return name
        checked = self.check_close_name(name)
        return checked

    def check_close_name(self, name):
        """Checks if there are any possible solutions to mistyped name"""
        matches = get_close_matches(name, self.folder_list)
        if not matches:
            return False
        user_choice = input(f'Did you mean any of these? (Leave blank if no): {\
            ", ".join(matches)}; ')
        if not user_choice.strip():
            return False  # User declined suggestions
        # Simple direct check - no recursion
        return user_choice if user_choice in self.folder_list else False

main()
