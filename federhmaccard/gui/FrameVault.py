#!/usr/bin/env python3

from tkinter import *
from tkinter.messagebox import showerror
from tkinter import ttk

from .VaultSelector import VaultSelector
from .CustomizedLabelFrame import CustomizedLabelFrame
from .ValueEntry import ValueEntry

from ..pubsub import publish, subscribe



class FrameVault(Frame):

    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.vault_selector = VaultSelector(self)
        self.vault_selector.pack(side="top", fill="x", expand=False)

        tabs = ttk.Notebook(self)
        self.tabs = tabs
        self.tabs.pack(side="top", fill="both", expand=True)

        tab_hmac = Frame(tabs)
        tab_manage = Frame(tabs)

        tabs.add(tab_hmac, text="Password Generation")
        tabs.add(tab_manage, text="Advanced")

        unlock_frame = CustomizedLabelFrame(tab_hmac, text="Decrypt Vault")
        self.unlock_frame = unlock_frame
    
        self.lbl_prompt = Label(unlock_frame, text="Password:")
        self.lbl_prompt.grid(column=0, row=0, padx=10, pady=20, sticky="e")

        self.txt_password = ValueEntry(unlock_frame)
        self.txt_password.grid(column=1, row=0, padx=10, pady=20, sticky="ew")
        self.txt_password.value.set("password")

        self.btn_login = Button(unlock_frame, text="Decrypt")
        self.btn_login.grid(column=2, row=0, padx=10, pady=20, sticky="ew")
        self.btn_login.bind("<Button-1>", self.on_login_clicked)

        self.unlock_frame.pack(side="top", fill="x", expand=False)



        """
        self.btn_init = Button(self, text="Initialize...")
        self.btn_init.grid(column=0, row=2, padx=10, pady=20, sticky="news")

        self.btn_reencrypt = Button(self, text="Change password...")
        self.btn_reencrypt.grid(column=1, row=2, padx=10, pady=20, sticky="news")
        """

        self.__bind_events()

    def __bind_events(self):
        subscribe("card/vault/status", self.on_vault_status_updated)
        subscribe("error/vault/wrong-password", self.on_wrong_password)

    def on_login_clicked(self, *args):
        password = self.txt_password.value.get()
        publish("card/do/vault/open", password)

    def on_vault_status_updated(self, status):
        if not status["success"]: return
        active_vault = status["vault"]
        vault_opened = status["open"]

        self.unlock_frame.enable(not vault_opened)

    def on_wrong_password(self):
        showerror(title="Error", message="Wrong password or the given vault is not initialized.")
