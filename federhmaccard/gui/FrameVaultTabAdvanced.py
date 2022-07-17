#!/usr/bin/env python3

import base64
import re

from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog

from .ValueEntry import ValueEntry
from .CustomizedLabelFrame import CustomizedLabelFrame
from ..pubsub import publish, subscribe

IMPORT_FORMATS = ["ASCII", "HEX", "Base32", "Base64"]


class TabAdvanced(Frame):
    
    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.frame_import = CustomizedLabelFrame(self, text="Import secret")

        self.frame_import.columnconfigure(0, weight=1)
        self.frame_import.columnconfigure(1, weight=1)
        self.frame_import.columnconfigure(2, weight=1)

        self.lbl_import_warning = Label(
            self.frame_import,
            text="Warning: this will overwrite existing secret!"
        )
        self.lbl_import_warning.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.import_secret = ValueEntry(self.frame_import)
        self.import_secret.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.import_format = ttk.Combobox(
            self.frame_import, values=IMPORT_FORMATS, state="readonly")
        self.import_format.grid(row=1, column=2, sticky="ew")
        self.import_format.current(0)

        self.import_desc = Label(self.frame_import, text="\n".join([
            "Notes:",
            "1. This operation will write a secret to the vault. ",
            "The written secret is not retractable from the vault.",
            "2. Any existing secret in this vault will be lost. ",
            "If you have no backup of that secret, do not import!",
            "3. If you intend to use the vault for TOTP based verification",
            " codes, you may need to select Base32 encoding."
        ]))
        self.import_desc.grid(row=2, column=0, columnspan=3, sticky="news")

        self.btn_import = Button(self.frame_import, text="Import")
        self.btn_import.grid(row=3, column=1, sticky="ew")
        self.btn_import.bind("<Button-1>", self.on_import_secret)

        
        self.frame_import.pack(side="top", fill="x", expand=False)
        subscribe("error/vault/failed-import", self.on_import_failure)
        subscribe("result/import/ok", self.on_import_ok)

    def on_import_failure(self, *args):
        messagebox.showerror("Error", "Failed to import secret.")

    def on_import_ok(self, *args):
        messagebox.showinfo("Success", "Vault initialized with new secret.")
        self.import_secret.value.set("")

    def on_import_secret(self, *args):
        newsecret = self.import_secret.value.get().strip()
        secretformat = IMPORT_FORMATS[self.import_format.current()]

        try:
            print("#1")
            assert re.match("^[\x20-\x7e]+$", newsecret)
            if secretformat == "Base32":
                print("#2")
                newsecret += ("=" * ((8 - (len(newsecret) % 8)) % 8))
                print("#3", newsecret)
                newsecret = base64.b32decode(newsecret, casefold=True)
            elif secretformat == "Base64":
                newsecret = base64.b64decode(newsecret)
            elif secretformat == "HEX":
                newsecret = bytes.fromhex(newsecret)
            assert len(newsecret) <= 64
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "New secret does not match selected format. Or it must not be longer than 64 bytes.")
            return

        if not newsecret:
            messagebox.showerror("Error", "Cannot import empty secret.")
            return
        if messagebox.askquestion("Confirm", "This will overwrite any secret on card! Are you sure to continue?") != "yes":
            return
        if simpledialog.askstring("Confirm again", "Type the word CONFIRM in uppercase to continue.", parent=self) != "CONFIRM":
            return

        publish("card/do/vault/import", newsecret)
        
