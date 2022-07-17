#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from .ValueEntry import ValueEntry
from .ValueCheck import ValueCheck
import hashlib
import base64


LENGTHS = [8, 12, 16, 20, 24, 28, 32, 64, 128]
class PasswordGen(ttk.LabelFrame):

    def __init__(self, parent, *args, **kvargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kvargs)

        self.__seed = None

        for i in range(1, 5): self.columnconfigure(i, weight=1)

        ROW = 0

        self.result = ValueEntry(self, state="readonly", font=("monospace", 16))
        self.result.grid(row=ROW, column=0, columnspan=5, sticky="we", pady=20)

        ROW += 1

        Label(self, text="Length").grid(row=ROW, column=0, sticky="news")
        Label(self, text="A-Z").grid(row=ROW, column=1, sticky="news")
        Label(self, text="a-z").grid(row=ROW, column=2, sticky="news")
        Label(self, text="0-9").grid(row=ROW, column=3, sticky="news")
        Label(self, text="*#?").grid(row=ROW, column=4, sticky="news")

        ROW += 1
            
        self.pwdlength = ttk.Combobox(
            self, values=[str(e) for e in LENGTHS], state="readonly")
        self.pwdlength.current(3)
        self.pwdlength.grid(row=ROW, column=0, sticky="news")

        self.charaz = ValueCheck(self)
        self.charaz.grid(row=ROW, column=1, sticky="news")
        self.charaz.value.set(True)

        self.charAZ = ValueCheck(self)
        self.charAZ.grid(row=ROW, column=2, sticky="news")
        self.charAZ.value.set(True)

        self.char09 = ValueCheck(self)
        self.char09.grid(row=ROW, column=3, sticky="news")
        self.char09.value.set(True)

        self.charspecial = ValueCheck(self)
        self.charspecial.grid(row=ROW, column=4, sticky="news")
        self.charspecial.value.set(True)

        for e in [
            self.pwdlength, self.charaz,
            self.charAZ, self.char09, self.charspecial
        ]:
            e.bind("<ButtonRelease>", self.update_result)
            e.bind("<Key>", self.update_result)

    def seed(self, s):
        self.__seed = s 
        self.update_result()

    def update_result(self, *args):
        if not self.__seed: return self.result.value.set("")

        def randomness():
            x = self.__seed
            while True:
                yield base64.b85encode(x).decode("ascii")
                x = hashlib.sha256(x).digest()

        length_required = LENGTHS[self.pwdlength.current()]
        assert length_required > 0
        result = ""

        with_az = self.charaz.value.get()
        with_AZ = self.charAZ.value.get()
        with_09 = self.char09.value.get()
        with___ = self.charspecial.value.get()
        
        if not (with_az or with_AZ or with_09 or with___):
            return self.result.value.set("")

        rng = randomness()
        while len(result) < length_required:
            feed = next(rng)
            while feed != "":
                c = feed[0]
                feed = feed[1:]
                if with_az and c in "abcdefghijklmnopqrstuvwxyz":
                    result += c
                if with_AZ and c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    result += c
                if with_09 and c in "0123456789":
                    result += c
                if with___ and c.lower() not in "0123456789abcdefghijklmnopqrstuvwxyz":
                    result += c
                
        self.result.value.set(result[:length_required])
