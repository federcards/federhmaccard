#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from .PasswordGen import PasswordGen
from .ValueEntry import ValueEntry
from ..pubsub import publish, subscribe


class TabPasswordgen(Frame):
    
    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        ROW = 0

        self.result = PasswordGen(self, text="Password Generator")
        self.result.grid(
            row=ROW, column=0, columnspan=3, sticky="news",
            padx=10, pady=10, ipadx=10, ipady=10)

        ROW += 1

        self.lbl_salt = Label(self, text="Salt")
        self.lbl_salt.grid(row=ROW, column=0)

        self.lbl_algo = Label(self, text="Algorithm")
        self.lbl_algo.grid(row=ROW, column=1)

        ROW += 1

        self.salt = ValueEntry(self)
        self.salt.grid(row=ROW, column=0, sticky="we")

        self.algo = ttk.Combobox(self, values=["SHA1", "SHA256"], state="readonly")
        self.algo.grid(row=ROW, column=1, sticky="we")
        self.algo.current(0)

        self.btn_generate = Button(self, text="Generate")
        self.btn_generate.grid(row=ROW, column=2, sticky="we")
        self.btn_generate.bind("<Button-1>", self.on_generate_clicked)


        self.__bind_events()

    def on_generate_clicked(self, *args):
        salt = self.salt.value.get()
        algo = ["sha1", "sha256"][self.algo.current()]
        publish("card/do/vault/hmac-%s" % algo, salt)

    def __bind_events(self):
        subscribe("result/hmac/sha1", self.on_hmac_sha1_result)
        subscribe("result/hmac/sha256", self.on_hmac_sha256_result)

    def on_hmac_sha1_result(self, digest):
        self.__show_result("SHA1", digest)

    def on_hmac_sha256_result(self, digest):
        self.__show_result("SHA256", digest)

    def __show_result(self, algo, digest):
        self.result.seed(digest)
