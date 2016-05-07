# -*- coding: utf-8 -*-
import wx
import operator


class DocPageEditDialog(wx.Dialog):
    def __init__(self, parent, id, title, commentsIdx):
        """
        :param parent:
        :param id:
        :param title:
        :type commentsIdx: dict
        :return:
        """
        dialogW = 400
        dialogH = 100
        wx.Dialog.__init__(self, parent, id, title, size=(dialogW, dialogH))
        panel = wx.Panel(self, -1)
        self.commentsIdx = commentsIdx
        # vbox = wx.BoxSizer(wx.VERTICAL)
        self.statusCb = wx.ComboBox(panel, -1, pos=(5, 5), size=(dialogW-10, 28))
        self.statusCb.Append("no change")
        self.statusCb.Append("progress")
        self.statusCb.Append("regress")
        self.statusCb.SetSelection(0)
        self.commentCb = wx.ComboBox(panel, -1, pos=(5, 38), size=(dialogW-10, 28))
        if len(commentsIdx) > 0:
            sortedIdx = sorted(commentsIdx.items(), key=operator.itemgetter(1))
            comments, freq = zip(*sortedIdx)
            self.commentCb.AppendItems(comments.reverse())
        # vbox.Add(self.statusCb, proportion=1)
        # self.SetSizer(vbox)
