# -*- coding: utf-8 -*-
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

        self.commentFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.commentFont.SetPointSize(9)
        self.commentFont.SetFaceName("sans")

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

        if doc.isCompared():
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(wx.TRANSPARENT_BRUSH if not doc.isCompared() else wx.Brush(wx.Colour(125, 125, 125)) )
            dc.DrawRectangle(rect.x + 1, rect.y + 2, 5, rect.height - 3)

        labelRect = wx.Rect(rect.x + 20, rect.y + 2, rect.width - 20, rect.height / 2 - 4)
        commentRect = wx.Rect(labelRect.x, labelRect.y + labelRect.height + 2, labelRect.width, labelRect.height)

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetFont(self.labelFont)
        dc.SetTextForeground(wx.BLACK)
        dc.DrawLabel(doc.key, labelRect)
        dc.SetFont(self.commentFont)
        if doc.comment is None or len(doc.comment) == 0:
            dc.SetTextForeground(wx.RED)
            dc.DrawLabel("not commented", commentRect)
        else:
            dc.SetTextForeground(wx.BLUE)
            dc.DrawLabel(doc.comment, commentRect)


    def GetItem(self, index):
        return self.docs[index]

