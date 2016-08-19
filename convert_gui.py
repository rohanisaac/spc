#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI verions of convert.py using Tkinter

Notes:
Only takes a single directory as input

author: Rohan Isaac
"""

from __future__ import division, absolute_import, unicode_literals, print_function
from Tkinter import Tk, StringVar, DISABLED, NORMAL, END, W, E, N, S
from ttk import Frame, Label, Button, Radiobutton, Entry
import tkFileDialog
import spc
import os


class ConvertSPC:
    def __init__(self, master):
        self.master = master
        master.title("Convert SPC files")

        mf = Frame(master, padding="10")
        mf.grid(column=0, row=0, sticky=(N, W, E, S))
        mf.columnconfigure(0, weight=1)
        mf.rowconfigure(0, weight=1)
        self.message = "Enter folder containing *.SPC files"
        self.label_text = StringVar()
        self.folder = StringVar()
        self.output_fmt = StringVar()

        self.label_text.set(self.message)

        self.label = Label(mf, textvariable=self.label_text)
        self.folder_label = Label(mf, text="Folder")
        self.output_fmt_label = Label(mf, text="Output Format")

        self.fmt_txt = Radiobutton(mf, text="TXT", variable=self.output_fmt, value='txt')
        self.fmt_csv = Radiobutton(mf, text="CSV", variable=self.output_fmt, value='csv')
        self.folder_entry = Entry(mf, textvariable=self.folder)

        self.sel_foler = Button(mf, text="Browse", command=self.ask_dir)
        self.convert_btn = Button(mf, text="Convert", command=self.convert)

        # map on grid
        self.label.grid(row=0, column=0, columnspan=4, sticky=W + E)
        self.folder_label.grid(row=1, column=0, sticky=E)
        self.output_fmt_label.grid(row=2, column=0, sticky=E)
        self.folder_entry.grid(row=1, column=1, columnspan=2, sticky=W + E)
        self.fmt_txt.grid(row=2, column=1, sticky=W)
        self.fmt_csv.grid(row=2, column=2, sticky=W)
        self.sel_foler.grid(row=1, column=3, sticky=W)
        self.convert_btn.grid(row=3, column=1, columnspan=2, sticky=W + E)

        for child in mf.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def convert(self):
        self.fol_val = str(self.folder.get())
        self.fmt_val = str(self.output_fmt.get())
        print("About to convert {} with {} ext".format(self.fol_val, self.fmt_val))

        if self.fmt_val == 'txt':
            exten = '.txt'
            delim = '\t'
        else:
            # defaults
            exten = '.csv'
            delim = ','

        flist = []

        # only directory here
        ffn = os.path.abspath(self.fol_val)
        for f in os.listdir(ffn):
            flist.append(os.path.join(ffn, f))

        # process files
        for fpath in flist:
            if fpath.lower().endswith('spc'):

                foutp = fpath[:-4] + exten
                try:
                    print(fpath, end=' ')
                    f = spc.File(fpath)
                    f.write_file(foutp, delimiter=delim)
                    print('Converted')
                except:
                    print('Error processing %s' % fpath)
            else:
                print('%s not spc file, skipping' % fpath)

    def ask_dir(self):
        self.folder.set(tkFileDialog.askdirectory())

if __name__ == "__main__":
    root = Tk()
    ConvertSPC(root)
    root.mainloop()
