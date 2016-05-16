# -*- coding: utf-8 -*-

import wx
from diffviewer import DiffViewer, EVT_REQUEST_NEXT, EVT_DOCPAGE_CHANGED
from docpage import DocPage
from doclist import DocListBox
from prefetcher import Prefetcher
from PIL import Image
from pprint import pprint
import cProfile
from settings import PREFETCH_COUNT

_KC_i = 73
_KC_j = 74
_KC_k = 75


def _loadimg(filename):
    scales = [66, 50, 33, 22]
    result = {}
    img = wx.Image(filename)
    w, h = img.GetSize()
    result[100] = wx.BitmapFromBuffer(w, h, img.GetData())
    for scale in scales:
        """@type : wx.Image"""
        sw, sh = int(w * scale * 0.01), int(h * scale * 0.01)
        img.Rescale(sw, sh, wx.IMAGE_QUALITY_BILINEAR)

        result[scale] = wx.BitmapFromBuffer(sw, sh, img.GetData())

    return result


class MyFrame(wx.Frame):
    def __init__(self, parent, title, docs):
        wx.Frame.__init__(self, parent, title=title)
        self._prefetcher = Prefetcher(_loadimg, 0.5, PREFETCH_COUNT * 3 + 3)
        self.InitUI(docs)
        self.Show(True)
        self.isEditing = False
        self.commentsIndex = {}
        self.updateCommentsIndex()
        self.prof = cProfile.Profile()

    def InitUI(self, docs):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.diffviewer = DiffViewer(self, "diffViewer", self._prefetcher)
        self.diffviewer.Bind(EVT_REQUEST_NEXT, self.onRequestNext)
        self.diffviewer.Bind(EVT_DOCPAGE_CHANGED, self.onDocPageChanged)
        self.filelist = DocListBox(self, docs)
        self.filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        self.filelist.Bind(wx.EVT_LISTBOX, self.onItemSelected)
        vbox.Add(self.filelist, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.CreateStatusBar(3)
        self.SetStatusWidths([55, 350, 70])

    def onItemClicked(self, event):
        self.show(event.GetSelection())

    def onDocPageChanged(self, event):
        self.updateCommentsIndex()

    def updateCommentsIndex(self):
        self.commentsIndex.clear()
        for docPage in self.filelist.docs:
            if docPage.hasComment():
                if docPage.comment in self.commentsIndex.keys():
                    self.commentsIndex[docPage.comment] += 1
                else:
                    self.commentsIndex[docPage.comment] = 1

    def show(self, idx):
        """
        :type idx: DocPage
        :return:
        """
        doc = self.filelist.GetItem(idx)
        if doc.ensureCompared():
            self.prof.runcall(self.diffviewer.load, doc, self.commentsIndex)
            self.prof.print_stats()
        for i in xrange(idx + 1, idx + PREFETCH_COUNT + 1):
            if i >= self.filelist.GetItemCount():
                break
            doc = self.filelist.GetItem(i)
            """
            @type: DocPage
            """
            if doc.ensureCompared():
                self._prefetcher.add(doc.imgBeforeFilename(), doc.imgBeforeFilename())
                self._prefetcher.add(doc.imgAfterFilename(), doc.imgAfterFilename())
                self._prefetcher.add(doc.imgDiffFilename(), doc.imgDiffFilename())


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
            return
        if event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, _KC_i]:
            self.show(self.filelist.GetSelection())
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
        self.show(self.filelist.GetSelection())

    def RefreshDocList(self):
        self.filelist.Refresh()

