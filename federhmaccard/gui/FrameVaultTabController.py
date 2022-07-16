#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from .ValueEntry import ValueEntry
from ..pubsub import publish, subscribe


class TabDecrypt(Frame):
    
    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)
        
        self.lbl_prompt = Label(self, text="Password:")
        self.lbl_prompt.grid(column=0, row=0, padx=10, pady=20, sticky="e")

        self.txt_password = ValueEntry(self)
        self.txt_password.grid(column=1, row=0, padx=10, pady=20, sticky="ew")
        self.txt_password.value.set("password")

        self.btn_login = Button(self, text="Decrypt")
        self.btn_login.grid(column=2, row=0, padx=10, pady=20, sticky="ew")
        self.btn_login.bind("<Button-1>", self.on_login_clicked)


    def on_login_clicked(self, *args):
        password = self.txt_password.value.get()
        publish("card/do/vault/open", password)







class FrameVaultTabController(ttk.Notebook):

    def __init__(self, parent, *args, **kvargs):
        ttk.Notebook.__init__(self, parent, *args, **kvargs)

        #self.tabs = tabs
        #Eself.tabs.pack(side="top", fill="both", expand=True)

        self.tab_decrypt = TabDecrypt(self)
        self.tab_hmac = Frame(self)
        self.tab_manage = Frame(self)
        
        self.add(self.tab_decrypt, text="Unlock vault")
        self.add(self.tab_hmac, text="Password Generation")
        self.add(self.tab_manage, text="Advanced")
        
        self.update_status()

    def update_status(self, vault_open=False):
        self.hide(0)
        self.hide(1)
        self.hide(2)
        if not vault_open:
            self.add(self.tab_decrypt, text="Unlock vault")
            self.select(self.tab_decrypt)
        else:
            self.add(self.tab_hmac, text="Password Generation")
            self.add(self.tab_manage, text="Advanced")
            self.select(self.tab_hmac)
