"""Converts app links to Bitwarden"""

import sys

print('Ensure your password file is in the current folder.')
PATH = input("Enter csv name: ")
HEADERS = [
    ["url","username","password"],

    ["folder","favorite","type","name",
    "notes","fields","reprompt","login_uri",
    "login_username","login_password","login_totp"]
]
with open(PATH, "r", encoding="utf-8") as in_file:
    header = next(in_file).rstrip().split(",")
    if header not in HEADERS:
        print("Invalid file format")
        sys.exit(1)
    idx = header.index('login_uri') if 'login_uri' in header else header.index('url')

    with open("converted_links.csv", 'w', encoding='utf-8') as out_file:
        out_file.write(','.join(header) + '\n')
        for line in in_file.readlines():
            line = line.rstrip().split(',')
            if line[idx].startswith('android://'):
                line[idx] = f"androidapp://{line[idx].rsplit('@')[-1].rstrip('/')}"

            out_file.write(','.join(line) + '\n')
