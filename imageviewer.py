import wx


class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.doc_bm = None
        """@type : wx.Bitmap"""
        self.doc_scaled_bm = None
        """@type : wx.Bitmap"""
        self.mdc = None
        """@type : wx.MemoryDC"""
        self.scale = -1.0
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOTION, self.onMousemove)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMousedown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseup)

        self.centerPointMovedHandler = None
        self.startPos = None
        """@type : wx.Point"""
        self.SetBackgroundColour(wx.Colour(200,200,200))
        self.offset = wx.Point()

    def load(self, filename):
        self.doc_bm = wx.Bitmap(filename)
        if self.scale < 0:
            self.setScale(1)

    def setScale(self, scale):
        self.scale = float(scale)
        bw, bh = self.doc_bm.GetSize()
        sw, sh = int(bw * self.scale), int(bh * self.scale)
        self.doc_scaled_bm = wx.EmptyBitmap(sw, sh)
        self.mdc = wx.MemoryDC(self.doc_scaled_bm)
        tdc = wx.MemoryDC(self.doc_bm)
        self.mdc.StretchBlit(0, 0, sw, sh, tdc, 0, 0, bw, bh)

    def translate(self, point):
        """
        :type point: wx.Point
        :rtype: wx.Point
        """
        x, y = point.Get()
        scale = self.scale
        point.Set(round(x / scale),round(y / scale))
        return point

    def getPaintParams(self):
        w, h = self.GetClientSize()
        sw, sh = self.mdc.GetSize()

        dx, dy = self.offset.Get()
        ddx, ddy = 0, 0
        if w > sw:
            dx = 0
            ddx = (w - sw) / 2
            w = sw
        if h > sh:
            dy = 0
            ddy = (h - sh) / 2
            h = sh
        return dx, dy, ddx, ddy, w, h


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
            self.centerPointMovedHandler((so + center - do)/self.scale)

    def onMousemove(self, event):
        if self.startPos is not None:
            self.offset = (self.startPos - event.GetPosition())
            self.Refresh()

    def onPaint(self, event):
        dc = wx.GCDC(self)
        mdc = self.mdc
        dc.Clear()
        dx, dy, ddx, ddy, w, h = self.getPaintParams()
        dc.Blit(ddx, ddy, w, h, mdc, dx, dy)
