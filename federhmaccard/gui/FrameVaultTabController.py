#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from .ValueEntry import ValueEntry
from ..pubsub import publish, subscribe

from .FrameVaultTabDecrypt import TabDecrypt
from .FrameVaultTabPasswordgen import TabPasswordgen
from .FrameVaultTabTOTP import TabTOTP


class FrameVaultTabController(ttk.Notebook):

    def __init__(self, parent, *args, **kvargs):
        ttk.Notebook.__init__(self, parent, *args, **kvargs)

        #self.tabs = tabs
        #Eself.tabs.pack(side="top", fill="both", expand=True)

        self.tab_decrypt = TabDecrypt(self)
        self.tab_pwdgen = TabPasswordgen(self)
        self.tab_totp = TabTOTP(self)
        self.tab_manage = Frame(self)
        
        self.add(self.tab_decrypt, text="Unlock vault")
        self.add(self.tab_pwdgen, text="Password Generator")
        self.add(self.tab_totp, text="Time-based Codes")
        self.add(self.tab_manage, text="Advanced")
        
        self.update_status()

    def update_status(self, vault_open=False):
        for i in range(0, 4): self.hide(i)
        if not vault_open:
            self.add(self.tab_decrypt)
            self.select(self.tab_decrypt)
        else:
            self.add(self.tab_pwdgen)#, text="Password Generation")
            self.add(self.tab_totp)
            self.add(self.tab_manage)#, text="Advanced")
            self.select(self.tab_pwdgen)
