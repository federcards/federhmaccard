#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

from .FrameWaitCard   import FrameWaitCard
from .FrameCardUnlock import FrameCardUnlock
from .FrameVault      import FrameVault


class FederHMACCard(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title("FederHMACCard: Password Generator")
        self.geometry("500x400")
        self.__init_widgets()

        self.card_ready = False
        self.card_unlocked = False

        self.switch_frame()

    def __init_widgets(self):
        kvargs = {}
        frame_wait = FrameWaitCard(self, **kvargs)
        frame_unlock = FrameCardUnlock(self, **kvargs)
        frame_vault = FrameVault(self, **kvargs)

        self.__frames = {
            "unlock": frame_unlock,
            "vault":  frame_vault,
            "wait": frame_wait,
        }

    def switch_frame(self):
        frame = "wait"
        if self.card_ready:
            if self.card_unlocked:
                frame = "vault"
            else:
                frame = "unlock"
        for fn in self.__frames:
            if fn == frame:
                self.__frames[fn].pack(fill="both", expand=True)
            else:
                self.__frames[fn].pack_forget()
            
