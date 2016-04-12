import wx


class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.doc_bm = None
        """@type : wx.Bitmap"""
        self.cached_doc_bm = None
        """
        internal original document representation with resolution reduced to optimize performance, kind of doc cache
        @type : wx.Bitmap
        """
        self.page_bm = None
        """
        fixed size page representing document with all additional elements on it
        @type : wx.Bitmap
        """
        self.mdc = None
        """@type : wx.MemoryDC"""
        self.scale = 1.0
        self.page_scale = -1.0
        self.is_fit_to_screen = True
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.pointer_pos = None
        """@type : wx.Point"""
        self.SetBackgroundColour(wx.Colour(200,200,200))

    def load(self, filename):
        self.doc_bm = doc_bm = wx.Bitmap(filename)
        self.page_scale = int_scale = min(2000 / (doc_bm.GetWidth() * 1.0), 2000 / (doc_bm.GetHeight() * 1.0))
        self.page_bm = wx.EmptyBitmap(doc_bm.GetWidth() * int_scale, doc_bm.GetHeight() * int_scale)
        self.cached_doc_bm = wx.EmptyBitmap(doc_bm.GetWidth() * int_scale, doc_bm.GetHeight() * int_scale)
        mdc = wx.MemoryDC(self.cached_doc_bm)
        image = wx.ImageFromBitmap(self.doc_bm)
        iw,ih = self.get_page_size()
        image = image.Scale(iw, ih, wx.IMAGE_QUALITY_BILINEAR)
        result = wx.BitmapFromImage(image)
        mdc.DrawBitmap(result, 0, 0)
        mdc.SelectObject(wx.NullBitmap)

        self.mdc = wx.MemoryDC(self.page_bm)
        self.mdc.SetUserScale(int_scale, int_scale)

    def save_image(self):
        self.page_bm.SaveFile("test.jpg", wx.BITMAP_TYPE_JPEG)

    def get_canvas_size(self):
        doc_bm = self.doc_bm
        return (doc_bm.GetWidth() * self.scale, doc_bm.GetHeight() * self.scale)

    def get_page_size(self):
        page_bm = self.page_bm
        return page_bm.GetWidth(), page_bm.GetHeight()

    def translate(self, point):
        """
        :type point: wx.Point
        :rtype: wx.Point
        """
        x,y = point.Get()
        scale = self.scale
        point.Set(round(x / scale),round(y / scale))
        return point

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        doc_w, doc_h = (self.doc_bm.GetWidth(), self.doc_bm.GetHeight())
        mdc = self.mdc
        if self.is_fit_to_screen:
            w, h = self.GetSize()
            self.scale = min(w / (doc_w * 1.0), h / (doc_h * 1.0))
        backColour = self.GetBackgroundColour()
        backBrush = wx.Brush(backColour, wx.SOLID)
        mdc.SetBackground(backBrush)
        mdc.Clear()
        dc.Clear()
        self.paint_image(mdc)
        cw, ch = self.get_canvas_size()
        iw, ih = self.get_page_size()
        mdc.SetUserScale(1.0,1.0)
        dc.StretchBlit(0,0, cw, ch, mdc, 0, 0, iw, ih)

    def paint_image(self, dc):
        if self.doc_bm is not None:
            dc.SetUserScale(self.scale, self.scale)
            dc.DrawBitmap(self.cached_doc_bm, 0, 0)
