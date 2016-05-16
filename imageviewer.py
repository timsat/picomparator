# -*- coding: utf-8 -*-
import wx


def div(point, divider):
    return wx.Point(round(point.x / divider), round(point.y / divider))


def mul(point, mult):
    return wx.Point(round(point.x * mult), round(point.y * mult))


class ImagePanel(wx.Panel):
    __labelPos = (10, 10)

    def __init__(self, parent, label, prefetcher):
        wx.Panel.__init__(self, parent)
        self._scaled_bitmaps = None
        self._prefetcher = prefetcher
        self.doc_scaled_bm = None
        """@type : wx.Bitmap"""
        self.scale = -1.0
        self.label = label
        self.offset = wx.Point()
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOTION, self.onMousemove)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMousedown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseup)

        self.centerPointMovedHandler = None
        self.startPos = None
        """@type : wx.Point"""
        self.SetBackgroundColour(wx.Colour(200, 200, 200))

    def load(self, filename):
        self._scaled_bitmaps = self._prefetcher.get(filename, filename)
        self.offset = wx.Point()

    def setScale(self, scale):
        self.scale = float(scale)
        """@type : wx.Image"""
        self.doc_scaled_bm = self._scaled_bitmaps[int(self.scale * 100)]
        self.Refresh()

    def translate(self, point):
        """
        :type point: wx.Point
        :rtype: wx.Point
        """
        x, y = point.Get()
        scale = self.scale
        point.Set(round(x / scale), round(y / scale))
        return point

    def getPaintParams(self):
        w, h = self.GetClientSize()
        # sw, sh = self.mdc.GetSize()

        dx, dy = self.offset.Get()
        ddx, ddy = 0, 0
        # if w > sw:
            # dx = 0
            # ddx = (w - sw) / 2
            # w = sw
        # if h > sh:
            # dy = 0
            # ddy = (h - sh) / 2
            # h = sh
        return dx, dy, ddx, ddy, w, h

    def moveCenterPoint(self, point):
        cw, ch = self.GetClientSize()
        dx, dy, ddx, ddy, w, h = self.getPaintParams()
        do = wx.Point(ddx, ddy)
        center = wx.Point(cw/2, ch/2)
        self.offset = mul(point, self.scale) - center + do
        self.Refresh()

    def onMousedown(self, event):
        self.startPos = event.GetPosition() + self.offset

    def onMouseup(self, event):
        self.startPos = None
        if self.centerPointMovedHandler is not None:
            cw, ch = self.GetClientSize()
            dx, dy, ddx, ddy, w, h = self.getPaintParams()
            so = wx.Point(dx, dy)
            do = wx.Point(ddx, ddy)
            center = wx.Point(cw/2, ch/2)
            self.centerPointMovedHandler(div(so + center - do, self.scale))

    def onMousemove(self, event):
        if self.startPos is not None:
            self.offset = (self.startPos - event.GetPosition())
            self.Refresh()

    def onPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        mdc = wx.MemoryDC(self.doc_scaled_bm)
        dc.SetBackground(wx.Brush(wx.Colour(127, 127, 127)))
        dc.Clear()
        dx, dy, ddx, ddy, w, h = self.getPaintParams()
        if self.doc_scaled_bm.HasAlpha():
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.DrawRectangle(ddx, ddy, w, h)
        dc.Blit(ddx, ddy, w, h, mdc, dx, dy, useMask=self.doc_scaled_bm.HasAlpha())
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.Colour(250, 0, 0), 1))
        dc.DrawRectangle(0, 0, w, h)
        dc.DrawRectangle(w/2 - 20, h/2 - 20, 40, 40)
        lx, ly = ImagePanel.__labelPos
        lw, lh = dc.GetTextExtent(self.label)
        dc.SetBrush(wx.Brush(wx.Colour(255, 195, 195, 170)))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(lx, ly, lw+2, lh+2)
        dc.DrawText(self.label, lx+1, ly+1)

