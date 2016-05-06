# -*- coding: utf-8 -*-
import wx


class DocPageEditDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 100))
