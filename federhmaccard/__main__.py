#!/usr/bin/env python3

from .card_io import CardSession
from getpass import getpass

from .gui import *


x = FederHMACCard()

x.mainloop()


"""
with CardSession() as session:

    while True:
        password = b"federcard"
        if session.login(password):
            break
        password = getpass().encode("ascii")

    print("Login success! Welcome to use FEDERCARD/HMACCard.")

    with session.vault(1) as vault:
        print(vault.status)

        pwd = getpass("Password for vault #1").encode("ascii")
        
        if vault.open(pwd):
            print(vault.HMAC_SHA1(b'test').hex())

        else:
            print("Import secret.")
            vault.import_secret(getpass("Secret to be imported?").encode("ascii"))
"""
