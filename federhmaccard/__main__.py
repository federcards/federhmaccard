#!/usr/bin/env python3

from .card_io import CardSession
from getpass import getpass


with CardSession() as session:

    while True:
        password = b"federcard"
        if session.login(password):
            break
        password = getpass().encode("ascii")

    print("Login success! Welcome to use FEDERCARD/HMACCard.")

    with session.vault(1) as vault:
        pwd = getpass("Password for vault #1").encode("ascii")
        vault.open(pwd)
