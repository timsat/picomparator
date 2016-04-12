# -*- coding: utf-8 -*-

import wx
import time
import subprocess
import document


def _kill_proc(process):
    try:
        process.terminate()
    except Exception:
        pass

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title, names, docMap, clickHandler):
        wx.Frame.__init__(self, parent, title=title)
        self.InitUI(names)
        self.clickHandler = clickHandler
        self.docMap = docMap
        self.Show(True)
        self.process1 = None
        self.process2 = None
        self.process3 = None


    def InitUI(self, names):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        font.SetFaceName("Liberation Mono")
        self.filelist = wx.ListBox(self, size=(700,500))
        self.filelist.InsertItems(names, 0)
        self.filelist.SetFont(font)
        self.filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        self.filelist.Bind(wx.EVT_LISTBOX, self.onItemSelected)
        hbox.Add(self.filelist, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(hbox)
        self.CreateStatusBar(3)
        self.SetStatusWidths([100,150,350])
        # self.statusbar = wx.StatusBar(self)
        # self.statusbar.SetFieldsCount()


    def onItemClicked(self, event):
        self.clickHandler(self, self.docMap[event.GetString()])

    def show(self, doc):
        if self.process1 is not None:
            _kill_proc(self.process1)
        if self.process2 is not None:
            _kill_proc(self.process2)
        if self.process3 is not None:
            _kill_proc(self.process3)

        if self.process1 is not None:
            self.process1.wait()
        if self.process2 is not None:
            self.process2.wait()
        if self.process3 is not None:
            self.process3.wait()


        imgs = doc.imgFiles()

        time.sleep(0.1)
        self.process1 = subprocess.Popen(["feh", "-d.", "-B", "white", imgs[0]])
        time.sleep(0.1)
        self.process2 = subprocess.Popen(["feh", "-d.", "-B", "white", imgs[1]])
        time.sleep(0.1)
        self.process3 = subprocess.Popen(["feh", "-d.", imgs[2]])


    def onItemSelected(self, event):
        doc = self.docMap[event.GetString()]
        self.SetStatusText(str(event.GetSelection()+3), 0)
        self.SetStatusText("processed" if doc.isCompared() else "not processed", 1)
        self.SetStatusText(doc.id(), 2)

