#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from .ValueEntry import ValueEntry
from ..pubsub import publish, subscribe
import struct
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
        num = int(time.time()) // interval 
        bstr = struct.pack('>Q', num)
        return bstr

    def __show_digits(self, digest, digits=6):
        offset = digest[-1] & 0xF
        token_base = digest[offset:offset+4]

        token_val = struct.unpack('>I', token_base)[0] & 0x7fffffff
        token_num = token_val % (10**digits)

        token = '{0:06d}'.format(token_num)
        return token

    def on_do_totp_sha1(self, *args):
        publish("card/do/vault/totp-sha1", self.__timecode())

    def on_totp_sha1_result(self, code):
        self.result.config(text=self.__show_digits(code, 8))
