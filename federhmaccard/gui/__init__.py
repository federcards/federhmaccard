#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

from ..pubsub import publish, subscribe

from .FrameWaitCard   import FrameWaitCard
from .FrameCardUnlock import FrameCardUnlock
from .FrameVault      import FrameVault


class FederHMACCard(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.width = 1000
        self.height = 600

        self.title("FederHMACCard: Password Generator")
        self.geometry("%dx%d" % (self.width, self.height))
        self.__init_widgets()

        self.card_ready = False
        self.card_unlocked = False

        self.switch_frame()
        self.__bind_events()

    def __init_widgets(self):
        kvargs = { "width": self.width, "height": self.height }
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
            
    def __bind_events(self):
        def on_card_status(newstatus):
            if newstatus == "disconnected":
                self.card_ready = False
                self.card_unlocked = False
            if newstatus == "connected":
                self.card_ready = True
                self.card_unlocked = False
            if newstatus == "unlocked":
                self.card_unlocked = True
                self.card_ready = True
            if newstatus == "locked":
                self.card_unlocked = False
                self.card_ready = True
            self.switch_frame()
                
        subscribe("card/status", on_card_status)
