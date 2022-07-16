#!/usr/bin/env python3

import threading
import queue
import time

from .card_io import CardSession
from .gui import FederHMACCard
from .pubsub import publish, subscribe


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = FederHMACCard() 
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

app = App()

##############################################################################

card_session = None
vault = None
def run_card_session():
    global card_session

    publish("card/status", "disconnected")
    print("Waiting for card...")

    with CardSession() as card_session:
        print("Card connected.")
        publish("card/status", "connected")

        password = b"federcard"
        if card_session.login(password):
            publish("card/status", "unlocked")
        else:
            publish("card/status", "locked")

        while True:
            time.sleep(0.5)

def autorestart_card_session():
    while True:
        try:
            run_card_session()
        except KeyboardInterrupt as e:
            exit()
        except:
            pass

threading.Thread(target=autorestart_card_session).start()

##############################################################################

def call_card_login(password):
    if not card_session: return
    print("Doing card login...")
    if card_session.login(password):
        publish("card/status", "unlocked")
    else:
        publish("card/status", "locked")
subscribe("card/do/login", call_card_login)


def call_select_vault(vault_id):
    if not card_session: return
    vault = card_session.vault(vault_id)
    publish("card/vault/status", vault.status)
subscribe("card/do/vault/select", call_select_vault)


def call_vault_open(password):
    if not card_session or not vault: return
    vault.open(password)
    publish("card/vault/status", vault.status)
subscribe("card/do/vault/open", call_vault_open)
