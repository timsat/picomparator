# -*- coding: utf-8 -*-

import wx
from diffviewer import DiffViewer, EVT_REQUEST_NEXT
from docpage import DocPage
from doclist import DocListBox
from pprint import pprint
from docpageeditdialog import DocPageEditDialog

_KC_i = 73
_KC_j = 74
_KC_k = 75

class MyFrame(wx.Frame):
    def __init__(self, parent, title, docs):
        wx.Frame.__init__(self, parent, title=title)
        self.InitUI(docs)
        self.Show(True)
        self.isEditing = False

    def InitUI(self, docs):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.diffviewer = DiffViewer(self, "diffViewer")
        self.diffviewer.Bind(EVT_REQUEST_NEXT, self.onRequestNext)
        self.filelist = DocListBox(self, docs)
        self.filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        self.filelist.Bind(wx.EVT_LISTBOX, self.onItemSelected)
        vbox.Add(self.filelist, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.CreateStatusBar(3)
        self.SetStatusWidths([55, 350, 70])
        self.docPageEditor = DocPageEditDialog(self, -1, "some title", {})

    def onItemClicked(self, event):
        self.show(self.filelist.GetItem(event.GetSelection()))

    def show(self, doc):
        """
        :type doc: DocPage
        :return:
        """
        if doc.ensureCompared():
            self.diffviewer.load(doc)

    def onItemSelected(self, event):
        doc = self.filelist.GetItem(event.GetSelection())
        """
        @type: Document
        """
        self.SetStatusText(str(event.GetSelection()+3), 0)
        self.SetStatusText(doc.id, 1)
        self.SetStatusText(str(doc.difference), 2)

    def onKeyDown(self, event):
        """
        :type event: wx.KeyEvent
        """
        print(event.GetKeyCode())
        if not self.IsActive():
            self.diffviewer.onKeyUp(event)
        if event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, _KC_i]:
            self.show(self.filelist.GetItem(self.filelist.GetSelection()))
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            pass
        elif event.GetKeyCode() == _KC_j:
            self.gotoNext()
        elif event.GetKeyCode() == _KC_k:
            self.gotoPrev()
        else:
            self.diffviewer.onKeyUp(event)

    def gotoNext(self):
        fl = self.filelist
        count = fl.GetItemCount()
        curIdx = fl.GetSelection()
        nextIdx = curIdx + 1 if curIdx < count - 1 else count - 1
        fl.SetSelection(nextIdx)

    def gotoPrev(self):
        fl = self.filelist
        curIdx = fl.GetSelection()
        nextIdx = curIdx - 1 if curIdx > 0 else 0
        fl.SetSelection(nextIdx)

    def onRequestNext(self, evt):
        self.gotoNext()
        self.show(self.filelist.GetItem(self.filelist.GetSelection()))

    def RefreshDocList(self):
        self.filelist.Refresh()

