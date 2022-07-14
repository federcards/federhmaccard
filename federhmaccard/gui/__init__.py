#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

from .FrameCardUnlock import FrameCardUnlock
from .FrameVault      import FrameVault


class FederHMACCard(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title("FederHMACCard: Password Generator")
        self.__init_widgets()


    def __init_widgets(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)

        self.columnconfigure(0, weight=1)

        self.txt_log = Text(self, height=10)
        self.txt_log.grid(row=0, column=0, padx=10, pady=10, sticky="news")

        self.frame_unlock = FrameCardUnlock(self)
        self.frame_unlock.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


        self.frame_vault = FrameVault(self)
        self.frame_vault.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
