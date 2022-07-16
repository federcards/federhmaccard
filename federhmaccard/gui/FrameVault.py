#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

class FrameVault(Frame):

    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)



        self.lbl_prompt = Label(self, text="Vault decrypt password:")
        self.lbl_prompt.grid(column=0, row=0, padx=10, pady=20, sticky="e")

        self.txt_password = Entry(self)
        self.txt_password.grid(column=1, row=0, padx=10, pady=20, sticky="ew")

        self.btn_login = Button(self, text="Decrypt Vault")
        self.btn_login.grid(column=2, row=0, padx=10, pady=20, sticky="ew")


        self.separator1 = ttk.Separator(self, orient="horizontal")
        self.separator1.grid(column=0, columnspan=3, row=1, sticky="ew")


        self.btn_init = Button(self, text="Initialize...")
        self.btn_init.grid(column=0, row=2, padx=10, pady=20, sticky="news")

        self.btn_reencrypt = Button(self, text="Change password...")
        self.btn_reencrypt.grid(column=1, row=2, padx=10, pady=20, sticky="news")
