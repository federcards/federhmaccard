#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from .ValueEntry import ValueEntry
from ..pubsub import publish, subscribe
import time


class TabTOTP(Frame):
    
    def __init__(self, parent, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.result = Label(self, text="------")
        self.btn_update = Button(self, text="Update")

        self.result.pack(side="top", expand=False, fill="x")
        self.btn_update.pack(side="top", expand=False, fill=None)
        
        self.btn_update.bind("<Button-1>", self.on_do_totp_sha1)
        #("card/do/vault/totp-sha1", call_vault_totp_sha1)


        subscribe("result/totp/sha1", self.on_totp_sha1_result)

        
    def __timecode(self, interval=30):
        now = int(time.time() / 30)
        bstr = b""
        while now != 0:
            bstr = bytes([now & 0xFF]) + bstr
            now >>= 8
        bstr = bstr.rjust(8, b"\x00")
        return bstr

    def on_do_totp_sha1(self, *args):
        publish("card/do/vault/totp-sha1", self.__timecode())

    def on_totp_sha1_result(self, code):
        code = code[:4]
        number = (code[0] << 24) | (code[1] << 16) | (code[2] << 8) | code[3]
        self.result.config(text=str(number % (10**6)))
