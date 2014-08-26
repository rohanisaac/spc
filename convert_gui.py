#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Graphical inteface for converter using wx

@author: Rohan Isaac
"""

import wx

def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.MULTIPLE
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPaths()
    else:
        path = None
    dialog.Destroy()
    return path

def get_dir():
    app = wx.App(None)
    style = wx.DD_DIR_MUST_EXIST
    dialog = wx.DirDialog(None, 'Open', style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

print get_path('Thermo Grams Spectra files (.spc) |*.spc')

print get_dir()
