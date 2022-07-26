#!/usr/bin/env python3
import csv
from tkinter import *
from tkinter import ttk


class PasswordTreeview(ttk.Treeview):

    def __init__(self, parent, csv, *args, **kvargs):
        kvargs["show"] = "tree" 
        kvargs["columns"] = ["#0", "Description", "URI"]
        ttk.Treeview.__init__(self, parent, *args, **kvargs)

        self.ybar = Scrollbar(parent, orient=VERTICAL, command=self.yview)
        self.configure(yscroll=self.ybar.set)

        #self.column("#0")
        #self.column("Description")
        #self.column("URI")
        self.heading("#0", text="Title", anchor="w")
        self.heading("Description", text="Description", anchor="w")
        self.heading("URI", text="URI", anchor="w")

        self.rows = {}
        self._load_csv(csv)


    def _load_csv(self, csvpath):
        rows = []

        with open(csvpath, newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) < 2: continue
                title = row[0]
                uri = row[1]
                path = tuple(["",] + row[2:])
                rows.append((title, uri, path))
        paths = list(set([e[2] for e in rows]))
        path_id = {
            ("",): ""
        }
        i = 1
        for pathtuple in paths:
            path_id[pathtuple] = "path-%d" % i
            i += 1

        # add paths
        paths.sort(key=lambda e: len(e))

        for path in paths:
            parent_path = path[:-1]
            if parent_path == "":
                parent_path = ("",)
            parent_path_id = path_id[parent_path]
            iid = path_id[path]
            self.insert(parent_path_id, "end", iid=path_id[path], text=path[-1])

        # add items

        for row_i in range(0, len(rows)):
            row_id = "row-%d" % row_i
            self.rows[row_id] = rows[row_i]
            title, uri, path = rows[row_i]

            parent_path_id = path_id[path]
            self.insert(
                parent_path_id, "end", iid=row_id,
                text=title, values=("Alphanumeric",uri)
            )
