#!/bin/python2.7
# -*- coding: utf-8 -*-

import wx
import subprocess
import time

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title, filelist, diff_dir, news, olds):
        wx.Frame.__init__(self, parent, title=title)
        self.InitUI(filelist)
        self.Show(True)
        self.diff_dir = diff_dir
        self.process1 = None
        self.process2 = None
        self.process3 = None
        self.news = news
        self.olds = olds


    def InitUI(self, files):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        filelist = wx.ListBox(self, size=(700,500))
        filelist.InsertItems(files, 0)
        filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        hbox.Add(filelist, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(hbox)

    def onItemClicked(self, event):
        if self.process1 is not None:
            self.process1.terminate()
        if self.process2 is not None:
            self.process2.terminate()
        if self.process3 is not None:
            self.process3.terminate()

        if self.process1 is not None:
            self.process1.wait()
        if self.process2 is not None:
            self.process2.wait()
        if self.process3 is not None:
            self.process3.wait()

        time.sleep(0.1)
        self.process1 = subprocess.Popen(["feh", "-d.", self.olds[event.GetString()]])
        time.sleep(0.1)
        self.process2 = subprocess.Popen(["feh", "-d.", self.news[event.GetString()]])
        time.sleep(0.1)
        self.process3 = subprocess.Popen(["feh", "-d.", self.diff_dir + "/" + event.GetString()])


import argparse
import os.path
import string

def visit_dir(arg, dirname, names):
    for fn in names:
        filepath = dirname + "/" + fn
        if os.path.isfile(filepath) and os.path.splitext(fn)[1].lower() == arg[1]:
            strip_index=string.index(filepath, "/", 1)+1
            arg[0][filepath[strip_index:]]=filepath

def visit_diffs(arg, dirname, names):
    for fn in names:
        filepath = dirname + "/" + fn
        if os.path.isfile(filepath) and os.path.splitext(fn)[1].lower() == arg[1]:
            strip_index=string.index(filepath, "/", 1)+1
            arg[0].append(filepath[strip_index:])

parser = argparse.ArgumentParser(description="Compares images in 2 directories and browses them")
parser.add_argument("new_dir", help="directory with new images")
parser.add_argument("old_dir", help="second with old images")
parser.add_argument("diffs_dir", default="diffs", help="resulting directory")
args = parser.parse_args()

new_files={}
old_files={}
diff_files=[]

os.path.walk(args.new_dir, visit_dir, (new_files, ".png"))
os.path.walk(args.old_dir, visit_dir, (old_files, ".png"))

for k,v in new_files.items():
    diff_path = args.diffs_dir + "/" + k
    if not os.path.exists(diff_path):
        print "compare %s" % k
        diff_dir = os.path.split(diff_path)[0]
        if not os.path.exists(diff_dir):
            os.makedirs(diff_dir)
        if subprocess.call(["compare", v, old_files[k], diff_path]) != 0:
            open(diff_path, 'a').close()


os.path.walk(args.diffs_dir, visit_diffs, (diff_files, ".png"))

if len(diff_files) > 0:
    print "Starting image browser"
    app = wx.App(False)
    frame = MyFrame(None, "Files", diff_files, args.diffs_dir, new_files, old_files )
    app.MainLoop()

