#!/usr/bin/env python3

#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from ..pubsub import publish, subscribe
from ..password_request_uri import FederPRURI, FederPRURIAlgorithm,\
    FederPRURICombinations
from .PasswordTreeview import PasswordTreeview


class TabTreeview(Frame):
    
    def __init__(self, parent, csv=None, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.treeview = PasswordTreeview(self, csv=csv)
        self.treeview.pack(expand=True, fill="both")


    """
        self.__bind_events()

    def on_seed_invalidated(self, *args):
        self.result.seed(None)

    def on_generate_clicked(self, *args):
        salt = bytes.fromhex(self.salt.hexvalue.get())
        algo = ["sha1", "sha256"][self.algo.current()]
        publish("card/do/vault/hmac-%s" % algo, salt)

    def on_pru_changed(self, *args):
        self.pru.config(bg="white")

    def on_apply_pru(self, *args):
        try:
            pru = FederPRURI.fromstring(self.pru.get())
        except:
            self.pru.config(bg="red")
            return

        if pru.algorithm == FederPRURIAlgorithm.SHA256:
            self.algo.current(1)
        else:
            self.algo.current(0)

        self.salt.set_bytes_to_hex_value(pru.seed)

        c = pru.combinations
        self.result.charAZ.value.set(
            bool(c & FederPRURICombinations.UPPERCASE.value))
        self.result.charaz.value.set(
            bool(c & FederPRURICombinations.LOWERCASE.value))
        self.result.char09.value.set(
            bool(c & FederPRURICombinations.NUMERICAL.value))
        self.result.charspecial.value.set(
            bool(c & FederPRURICombinations.SPECIAL.value))

    def __bind_events(self):
        subscribe("result/hmac/sha1", self.on_hmac_sha1_result)
        subscribe("result/hmac/sha256", self.on_hmac_sha256_result)

    def on_hmac_sha1_result(self, digest):
        self.__show_result("SHA1", digest)

    def on_hmac_sha256_result(self, digest):
        self.__show_result("SHA256", digest)

    def __show_result(self, algo, digest):
        self.result.seed(digest)

    """
