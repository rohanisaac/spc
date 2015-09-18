#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Graphical interface for converter using wx

@author: Rohan Isaac
"""

import wx

class MainFrame(wx.Frame):
    def __init__(self, title="Convert SPC to TXT", size=(350,200)):
        wx.Frame.__init__(self, None, id=-1, title=title, size=size)

        frame_pnl = wx.Panel(self)

        btn1 = wx.Button(frame_pnl, label="Open files")      
        btn2 = wx.Button(frame_pnl, label="Open folder")
        
        # bind buttons to events
        self.Bind(wx.EVT_BUTTON, self.get_path, btn1)
        self.Bind(wx.EVT_BUTTON, self.get_dir, btn2)
        
        # Adds menubar
        menubar = wx.MenuBar()
        file = wx.Menu()
        convert = wx.Menu()
        
        # adds items
        file.Append(101, '&Open', 'Open a file')
        file.Append(102, '&Save', 'Save the document')
        file.AppendSeparator()
        file.Append(105, '&Quit', 'Quit the application')
        
        menubar.Append(file, '&File')
        menubar.Append(convert, '&Convert')
        
        self.SetMenuBar(menubar)
        
        #list  control
        #lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        #lc.InsertColumn(0, 'File Name')
        
        
        pnl_horSiz = wx.BoxSizer(wx.HORIZONTAL)
        pnl_horSiz.AddStretchSpacer() # for v centering
        pnl_horSiz.Add(btn1, flag=wx.ALIGN_CENTER) # for h centering
        pnl_horSiz.Add(btn2, flag=wx.ALIGN_CENTER)
        
        pnl_horSiz.AddStretchSpacer() # for vertical centering
        #pnl_horSiz.Add(lc, flag=wx.ALIGN_CENTER)
        frame_pnl.SetSizer(pnl_horSiz)
        frame_pnl.Layout()
        
    def get_path(self, event):
        print "works path"
        #app = wx.App(self)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.MULTIPLE
        dialog = wx.FileDialog(None, 'Open', wildcard='Thermo Grams Spectra files (.spc) |*.spc', style=style)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()
        else:
            path = None
        dialog.Destroy()
        self.path = path
        print path
        
    def get_dir(self, event):
        print "works dir"
        #app = wx.App(self)
        style = wx.DD_DIR_MUST_EXIST
        dialog = wx.DirDialog(None, 'Open', style=style)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            path = None
        dialog.Destroy()
        self.path = path
        print path
        
if __name__ == '__main__' :
    app = wx.PySimpleApp( redirect=False)
    appFrame = MainFrame().Show()
    app.MainLoop()

