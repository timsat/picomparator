# -*- coding: utf-8 -*-

import wx
from diffviewer import DiffViewer


class MyFrame(wx.Frame):
    def __init__(self, parent, title, names, docMap, clickHandler):
        wx.Frame.__init__(self, parent, title=title)
        self.InitUI(names)
        self.clickHandler = clickHandler
        self.docMap = docMap
        self.Show(True)

    def InitUI(self, names):
        vbox = wx.BoxSizer(wx.VERTICAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        font.SetFaceName("Liberation Mono")
        self.diffviewer = DiffViewer(self, "diffViewer")
        self.filelist = wx.ListBox(self, size=(-1, -1), pos=(-1, -1))
        self.filelist.InsertItems(names, 0)
        self.filelist.SetFont(font)
        self.filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        self.filelist.Bind(wx.EVT_LISTBOX, self.onItemSelected)
        vbox.Add(self.filelist, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.CreateStatusBar(4)
        self.SetStatusWidths([55, 100, 350, 70])

    def onItemClicked(self, event):
        self.clickHandler(self, self.docMap[event.GetString()])

    def show(self, doc):
        imgs = doc.imgFiles()
        self.diffviewer.load(imgs[2], imgs[1], imgs[0])

    def onItemSelected(self, event):
        doc = self.docMap[event.GetString()]
        self.SetStatusText(str(event.GetSelection()+3), 0)
        self.SetStatusText("processed" if doc.isCompared() else "not processed", 1)
        self.SetStatusText(doc.id(), 2)
        self.SetStatusText(str(doc.diff), 3)

    def onKeyUp(self, event):
        self.diffviewer.onKeyUp(event)

