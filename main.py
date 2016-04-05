#!/bin/python2.7
# -*- coding: utf-8 -*-

import wx
import subprocess
import time

def _kill_proc(process):
    try:
        process.terminate()
    except Exception:
        pass

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
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        font.SetFaceName("Liberation Mono")
        filelist = wx.ListBox(self, size=(700,500))
        filelist.InsertItems(files, 0)
        filelist.SetFont(font)
        filelist.Bind(wx.EVT_LISTBOX_DCLICK, self.onItemClicked)
        hbox.Add(filelist, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(hbox)


    def onItemClicked(self, event):
        if self.process1 is not None:
            _kill_proc(self.process1)
        if self.process2 is not None:
            _kill_proc(self.process2)
        if self.process3 is not None:
            _kill_proc(self.process3)

        if self.process1 is not None:
            self.process1.wait()
        if self.process2 is not None:
            self.process2.wait()
        if self.process3 is not None:
            self.process3.wait()

        time.sleep(0.1)
        self.process1 = subprocess.Popen(["feh", "-d.", "-B", "white", self.olds[event.GetString()]])
        time.sleep(0.1)
        self.process2 = subprocess.Popen(["feh", "-d.", "-B", "white", self.news[event.GetString()]])
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
parser.add_argument("--file_list", default=None, help="file with list of images to compare", )
args = parser.parse_args()

new_files={}
old_files={}
diff_files=[]


if args.file_list is not None:
    with open(args.file_list, 'r') as f:
        for l in f:
            print "processing " + l
            full_new_path =  args.new_dir + "/" + l.strip("\n")[:-4]
            full_old_path =  args.old_dir + "/" + l.strip("\n")[:-4]
            strip_index=string.index(full_new_path, "/", 1)+1
            k = full_new_path[strip_index:] + ".png"

            if subprocess.call(["convert", "-density", "170", full_new_path, full_new_path + ".png"]) != 0:
                print "error converting " + full_new_path
            else:
                new_files[k] = full_new_path + ".png"

            if subprocess.call(["convert", "-density", "170", full_old_path, full_old_path + ".png"]) != 0:
                print "error converting " + full_old_path
            else:
                old_files[k] = full_old_path + ".png"
else:
    os.path.walk(args.new_dir, visit_dir, (new_files, ".png"))
    os.path.walk(args.old_dir, visit_dir, (old_files, ".png"))
    os.path.walk(args.diffs_dir, visit_diffs, (diff_files, ".png"))

print old_files

for k,v in new_files.items():
    diff_path = args.diffs_dir + "/" + k
    if not os.path.exists(diff_path):
        print "compare %s" % k
        diff_dir = os.path.split(diff_path)[0]
        if not os.path.exists(diff_dir):
            os.makedirs(diff_dir)
        if subprocess.call(["compare", v, old_files[k], diff_path]) != 0:
            open(diff_path, 'a').close()



if len(diff_files) > 0:
    print "Starting image browser"
    app = wx.App(False)
    frame = MyFrame(None, "Files", diff_files, args.diffs_dir, new_files, old_files )
    app.MainLoop()

