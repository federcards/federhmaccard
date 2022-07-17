#!/usr/bin/env python3

import threading
import queue
import time

from .card_io import CardSession
from .gui import FederHMACCard
from .pubsub import publish, subscribe, exit_flag


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        exit_flag.set()
        print("exit flag set. exiting.")
        publish("exit")
        #exit()
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
    global card_session, exit_flag

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

        while not exit_flag.is_set():
            time.sleep(0.5)

def autorestart_card_session():
    global exit_flag
    while not exit_flag.is_set():
        try:
            run_card_session()
        except KeyboardInterrupt as e:
            exit()
        except:
            pass
    print("Autorestart card session: finished.")

threading.Thread(target=autorestart_card_session).start()

##############################################################################

def _assert_bytes(s):
    if type(s) == str:
        return s.encode("ascii")
    if type(s) == bytes:
        return s
    raise Exception("Input parameter must be bytes.")

def call_card_login(password):
    global card_session, vault
    if not card_session: return
    print("Doing card login...")
    if card_session.login(_assert_bytes(password)):
        publish("card/status", "unlocked")
    else:
        publish("card/status", "locked")
subscribe("card/do/login", call_card_login)


def call_select_vault(vault_id):
    global card_session, vault
    if not card_session: return
    if vault:
        vault.close()
        publish("card/vault/status", vault.status)
    vault = card_session.vault(vault_id)
    publish("card/vault/status", vault.status)
subscribe("card/do/vault/select", call_select_vault)


def call_vault_open(password):
    global card_session, vault
    if not card_session or not vault: return
    print("open vault...")
    if not vault.open(_assert_bytes(password)):
        publish("error/vault/wrong-password")
    publish("card/vault/status", vault.status)
subscribe("card/do/vault/open", call_vault_open)


def call_vault_import(secret):
    global card_session, vault
    if not card_session or not vault: return
    if not vault.import_secret(_assert_bytes(secret)):
        publish("error/vault/failed-import")
    else:
        publish("result/import/ok")
    publish("card/vault/status", vault.status)
subscribe("card/do/vault/import", call_vault_import)


def call_vault_totp_sha1(seed):
    global card_session, vault
    if not card_session or not vault: return
    result = vault.HMAC_SHA1(_assert_bytes(seed))
    if not result:
        return publish("error/vault/locked")
    publish("result/totp/sha1", result)
subscribe("card/do/vault/totp-sha1", call_vault_totp_sha1)


def call_vault_hmac_sha1(seed):
    global card_session, vault
    if not card_session or not vault: return
    result = vault.HMAC_SHA1(_assert_bytes(seed))
    if not result:
        return publish("error/vault/locked")
    publish("result/hmac/sha1", result)
subscribe("card/do/vault/hmac-sha1", call_vault_hmac_sha1)


def call_vault_hmac_sha256(seed):
    global card_session, vault
    if not card_session or not vault: return
    result = vault.HMAC_SHA256(_assert_bytes(seed))
    if not result:
        return publish("error/vault/locked")
    publish("result/hmac/sha256", result)
subscribe("card/do/vault/hmac-sha256", call_vault_hmac_sha256)
