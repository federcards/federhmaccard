#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

class FrameCardUnlock(Frame):

    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        self.lbl_prompt = Label(self, text="Password:")
        self.lbl_prompt.grid(column=0, row=0, padx=10, pady=20, sticky="e")

        self.txt_password = Entry(self)
        self.txt_password.grid(column=1, row=0, padx=10, pady=20, sticky="ew")

        self.btn_login = Button(self, text="Login")
        self.btn_login.grid(column=2, row=0, padx=10, pady=20, sticky="ew")


        self.lbl_reset = Label(self, text="Dangerous! Do factory reset:", fg="red", anchor="e")
        self.lbl_reset.grid(column=0, columnspan=2, row=1, padx=10, pady=20, sticky="ew")

        self.btn_reset = Button(self, text="Factory Reset")
        self.btn_reset.grid(column=2, row=1, padx=10, pady=20, sticky="ew")
