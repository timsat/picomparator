import wx
from imageviewer import ImagePanel
from functools import partial


class DiffViewer(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.afterview = ImagePanel(self, "After")
        self.afterview.centerPointMovedHandler = partial(self._onAfterViewCenterPointMoved, self)
        self.beforeview = ImagePanel(self, "Before")
        self.beforeview.centerPointMovedHandler = partial(self._onBeforeViewCenterPointMoved, self)
        self.diffview = ImagePanel(self, "Difference")
        self.diffview.centerPointMovedHandler = partial(self._onDiffViewCenterPointMoved, self)
        self.scale = 0.5
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.beforeview, proportion=1, flag=wx.EXPAND | wx.ALL)
        vbox.Add(self.afterview, proportion=1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(self.diffview, proportion=1, flag=wx.EXPAND | wx.ALL)
        hbox.Add(vbox, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(hbox)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def load(self, nameAfter, nameBefore, nameDiff):
        self.afterview.load(nameAfter)
        self.beforeview.load(nameBefore)
        self.diffview.load(nameDiff)
        self.setScale(0.5)
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
