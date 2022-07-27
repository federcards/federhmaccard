#!/usr/bin/env python3

#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from ..pubsub import publish, subscribe
from ..password_request_uri import FederPRURI, FederPRURIAlgorithm,\
    FederPRURICombinations
from .PasswordTreeview import PasswordTreeview
from .PasswordResultDisplay import PasswordResultDisplay
from ..seed_to_password import seed2password
from ..password_request_uri import FederPRURI


class TabTreeview(Frame):
    
    def __init__(self, parent, csv=None, *args, **kvargs):
        Frame.__init__(self, parent, *args, **kvargs)

        self.treeview = PasswordTreeview(self, csv=csv)
        self.treeview.pack(expand=True, fill="both")

        self.result = PasswordResultDisplay(self)
        self.result.pack(expand=True, fill="x", side="top")

        self.treeview.value.trace_add("write", self.on_treeview_changed)

    def on_treeview_changed(self, *args):
        try:
            pruri = FederPRURI.fromstring(self.treeview.value.get())
        except Exception as e:
            print(e)
            return

        print(pruri)
