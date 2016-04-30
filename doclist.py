
import wx
from document import Document


class DocListBox(wx.VListBox):
    def __init__(self, parent, docs):
        super(DocListBox, self).__init__(parent)
        self.docs = docs
        self.SetItemCount(len(docs))

        self.labelFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.labelFont.SetPointSize(10)
        self.labelFont.SetFaceName("Liberation Mono")

    def OnMeasureItem(self, index):
        return 35

    def OnDrawSeparator(self, dc, rect, index):
        oldpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawLine(rect.x, rect.y, rect.x + rect.width, rect.y)

        dc.SetPen(oldpen)

    def OnDrawItem(self, dc, rect, index):
        '''
        :type dc: wx.DC
        :type rect: wx.Rect
        :type index: int
        '''
        doc = self.docs[index]
        """ @type: Document"""

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH if not doc.isCompared() else wx.Brush(wx.Colour(125, 125, 125)) )

        dc.DrawRectangle(rect.x + 1, rect.y + 2, 5, rect.height - 3)
        labelRect = wx.Rect(rect.x + 10, rect.y + 2, rect.width - 10, rect.height / 2 - 4)

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetFont(self.labelFont)
        dc.DrawLabel(doc.key, labelRect)

    def GetItem(self, index):
        return self.docs[index]

