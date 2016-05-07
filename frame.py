# -*- coding: utf-8 -*-

import wx
from diffviewer import DiffViewer
from docpage import DocPage
from doclist import DocListBox
from pprint import pprint
from docpageeditdialog import DocPageEditDialog

_KC_i = 73
_KC_j = 74
_KC_k = 75

class MyFrame(wx.Frame):
    def __init__(self, parent, title, docs, clickHandler):
        wx.Frame.__init__(self, parent, title=title)
        self.InitUI(docs)
        self.clickHandler = clickHandler
        self.Show(True)
        self.isEditing = False

    def InitUI(self, docs):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.diffviewer = DiffViewer(self, "diffViewer")
        self.filelist = DocListBox(self, docs)
        self.filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        self.filelist.Bind(wx.EVT_LISTBOX, self.onItemSelected)
        vbox.Add(self.filelist, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.CreateStatusBar(4)
        self.SetStatusWidths([55, 100, 350, 70])
        self.docPageEditor = DocPageEditDialog(self, -1, "some title", {})

    def onItemClicked(self, event):
        self.clickHandler(self, self.filelist.GetItem(event.GetSelection()))

    def show(self, doc):
        """
        :type doc: DocPage
        :return:
        """
        self.diffviewer.load(doc)

    def onItemSelected(self, event):
        doc = self.filelist.GetItem(event.GetSelection())
        """
        @type: Document
        """
        self.SetStatusText(str(event.GetSelection()+3), 0)
        self.SetStatusText("processed" if doc.isCompared() else "not processed", 1)
        self.SetStatusText(doc.id, 2)
        self.SetStatusText(str(doc.difference), 3)

    def onKeyDown(self, event):
        """
        :type event: wx.KeyEvent
        """
        print(event.GetKeyCode())
        if not self.IsActive():
            event.Skip()
            return
        if event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, _KC_i]:
            self.clickHandler(self, self.filelist.GetItem(self.filelist.GetSelection()))
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            pass
        elif event.GetKeyCode() == _KC_j:
            fl = self.filelist
            count = fl.GetItemCount()
            curIdx = fl.GetSelection()
            nextIdx = curIdx + 1 if curIdx < count - 1 else count - 1
            fl.SetSelection(nextIdx)
        elif event.GetKeyCode() == _KC_k:
            fl = self.filelist
            curIdx = fl.GetSelection()
            nextIdx = curIdx - 1 if curIdx > 0 else 0
            fl.SetSelection(nextIdx)
        else:
            self.diffviewer.onKeyUp(event)

    def RefreshDocList(self):
        self.filelist.Refresh()

