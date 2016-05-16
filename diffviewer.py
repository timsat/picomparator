# -*- coding: utf-8 -*-
import operator
import wx
from imageviewer import ImagePanel
from functools import partial
from docpage import DocPage

import wx.lib.newevent

RequestNextEvent, EVT_REQUEST_NEXT = wx.lib.newevent.NewEvent()
DocPageChangedEvent, EVT_DOCPAGE_CHANGED = wx.lib.newevent.NewEvent()

class DiffViewer(wx.Frame):
    def __init__(self, parent, title, prefetcher):
        wx.Frame.__init__(self, parent, title=title)
        self.afterview = ImagePanel(self, "After", prefetcher)
        self.afterview.centerPointMovedHandler = partial(self._onAfterViewCenterPointMoved, self)
        self.beforeview = ImagePanel(self, "Before", prefetcher)
        self.beforeview.centerPointMovedHandler = partial(self._onBeforeViewCenterPointMoved, self)
        self.diffview = ImagePanel(self, "Difference", prefetcher)
        self.diffview.centerPointMovedHandler = partial(self._onDiffViewCenterPointMoved, self)
        self.scale = 0.5
        self.doc = None
        """
        @type: DocPage
        """

        self.lastComment = ""
        self.lastStatus = ""

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        v2box = wx.BoxSizer(wx.VERTICAL)
        v2box.Add(self.beforeview, proportion=1, flag=wx.EXPAND | wx.ALL)
        v2box.Add(self.afterview, proportion=1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(self.diffview, proportion=1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(v2box, proportion=1, flag=wx.EXPAND | wx.ALL)

        panel = wx.Panel(self, -1)
        comboBoxesWidth = 400
        self.statusCb = wx.ComboBox(panel, -1, pos=(5, 5), size=(comboBoxesWidth, 28))
        self.statusCb.SetEditable(False)
        self.statusCb.Append("")
        self.statusCb.Append("no change")
        self.statusCb.Append("progress")
        self.statusCb.Append("regress")
        self.commentCb = wx.ComboBox(panel, -1, pos=(5, 38), size=(comboBoxesWidth, 28))
        self.fillLastBtn = wx.Button(panel, -1, label="Fill last", pos=(comboBoxesWidth + 10, 5), size=(28*4+5, 28*2+5))
        x, y = self.fillLastBtn.GetPositionTuple()
        w, h = self.fillLastBtn.GetSizeTuple()
        self.saveAndNextBtn = wx.Button(panel, -1, label="Save && next", pos=(x + w + 5, y), size=(28*4+5, 28*2+5))
        x, y = self.saveAndNextBtn.GetPositionTuple()
        w, h = self.saveAndNextBtn.GetSizeTuple()
        self.resetBtn = wx.Button(panel, -1, label="Reset", pos=(x + w + 5, 5), size=(28*2+5, 28*2+5))
        self.fillLastBtn.Bind(wx.EVT_BUTTON, self.onFillLast)
        self.saveAndNextBtn.Bind(wx.EVT_BUTTON, self.onSave)
        self.resetBtn.Bind(wx.EVT_BUTTON, self.onReset)

        vbox.Add(panel, flag=wx.EXPAND | wx.ALL)
        vbox.AddSpacer(5)
        vbox.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.CreateStatusBar(1)

    def load(self, doc, commentsIndex):
        """
        :type doc: DocPage
        :return:
        """
        self.doc = doc
        self.afterview.load(doc.imgAfterFilename())
        self.beforeview.load(doc.imgBeforeFilename())
        self.diffview.load(doc.imgDiffFilename())
        self.setScale(0.5)
        self.SetStatusText(doc.key)
        if len(commentsIndex.items()) > 0:
            kl = list(zip(*sorted(commentsIndex.items(), key=operator.itemgetter(1)))[0])
            kl.reverse()
            self.commentCb.Clear()
            self.commentCb.AppendItems(kl)
        self.onReset(None)
        self.Show(True)
        self.Refresh()

    def onKeyUp(self, event):
        if event.GetKeyCode() in [wx.WXK_ADD, wx.WXK_NUMPAD_ADD]:
            self.setScale(self.scale + 0.1)
        elif event.GetKeyCode() in [wx.WXK_SUBTRACT, wx.WXK_NUMPAD_SUBTRACT]:
            self.setScale(self.scale - 0.1)
        else:
            event.Skip()

    def onClose(self, event):
        self.Show(False)

    def onSave(self, event):
        self.lastComment = self.commentCb.GetValue()
        self.lastStatus = self.statusCb.GetValue()
        self.doc.update(self.lastStatus, self.lastComment)

        evt = DocPageChangedEvent()
        wx.PostEvent(self, evt)

        evt = RequestNextEvent()
        wx.PostEvent(self, evt)

    def onReset(self, event):
        self.commentCb.SetValue(self.doc.comment if self.doc.hasComment() else "")
        self.statusCb.SetValue(self.doc.status if self.doc.hasStatus() else "")

    def onFillLast(self, event):
        self.commentCb.SetValue(self.lastComment)
        self.statusCb.SetValue(self.lastStatus)

    def setScale(self, scale):
        if scale < 0.1:
            scale = 0.1
        self.scale = scale
        self.diffview.setScale(scale)
        self.afterview.setScale(scale)
        self.beforeview.setScale(scale)

    @staticmethod
    def _onDiffViewCenterPointMoved(self, point):
        self.afterview.moveCenterPoint(point)
        self.beforeview.moveCenterPoint(point)

    @staticmethod
    def _onBeforeViewCenterPointMoved(self, point):
        self.afterview.moveCenterPoint(point)
        self.diffview.moveCenterPoint(point)

    @staticmethod
    def _onAfterViewCenterPointMoved(self, point):
        self.diffview.moveCenterPoint(point)
        self.beforeview.moveCenterPoint(point)
