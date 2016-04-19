import wx
from imageviewer import ImagePanel
from functools import partial


class DiffViewer(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.diffview = ImagePanel(self)
        self.diffview.centerPointMovedHandler = partial(self.onDiffViewCenterPointMoved, self)
        self.beforeview = ImagePanel(self)
        self.beforeview.centerPointMovedHandler = partial(self.onBeforeViewCenterPointMoved, self)
        self.afterview = ImagePanel(self)
        self.afterview.centerPointMovedHandler = partial(self.onAfterViewCenterPointMoved, self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.beforeview, proportion=1, flag=wx.EXPAND | wx.ALL)
        vbox.Add(self.afterview, proportion=1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(self.diffview, proportion=1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(vbox, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(hbox)

    def load(self, nameDiff, nameBefore, nameAfter):
        self.diffview.load(nameDiff)
        self.afterview.load(nameAfter)
        self.beforeview.load(nameBefore)
        scale = 0.5
        self.diffview.setScale(scale)
        self.afterview.setScale(scale)
        self.beforeview.setScale(scale)
        self.Show(True)
        self.Refresh()

    def zoomIn(self, event):
        pass

    def zoomOut(self, event):
        pass

    @staticmethod
    def onDiffViewCenterPointMoved(self, point):
        self.afterview.moveCenterPoint(point)
        self.beforeview.moveCenterPoint(point)

    @staticmethod
    def onBeforeViewCenterPointMoved(self, point):
        self.afterview.moveCenterPoint(point)
        self.diffview.moveCenterPoint(point)

    @staticmethod
    def onAfterViewCenterPointMoved(self, point):
        self.diffview.moveCenterPoint(point)
        self.beforeview.moveCenterPoint(point)
