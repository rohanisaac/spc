#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Graphical inteface for converter using wx

@author: Rohan Isaac
"""

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(300, 250))

        panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)

        self.btn1 = wx.Button(panel1, -1, "Open files", pos=(50,100), size=(300,30))      
        self.btn2 = wx.Button(panel1, -1, "Open folder", pos=(50,150), size=(300,30))

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel1, 1, wx.EXPAND)


        self.btn1.Bind(wx.EVT_BUTTON, self.get_path())
        self.btn2.Bind(wx.EVT_BUTTON, self.get_dir())
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
    def get_path(self):
        app = wx.App(None)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.MULTIPLE
        dialog = wx.FileDialog(None, 'Open', wildcard='Thermo Grams Spectra files (.spc) |*.spc', style=style)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()
        else:
            path = None
        dialog.Destroy()
        return path
        
    def get_dir(self):
        app = wx.App(None)
        style = wx.DD_DIR_MUST_EXIST
        dialog = wx.DirDialog(None, 'Open', style=style)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            path = None
        dialog.Destroy()
        return path

app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Convert SPC to TXT")
frame.Show()
app.MainLoop()

