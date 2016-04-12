#!/bin/python2.7
# -*- coding: utf-8 -*-


import subprocess
import argparse
import os.path
import string
import wx
from threading import Thread
from frame import MyFrame
from document import Document
import Queue

class Task:
    def __init__(self, doc, priority=0):
        """
        :type doc: Document
        :type priority: int
        :return:
        """
        self.doc = doc
        # self.priority = priority


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


def convert(srcFile, imgFile):
    if (not os.path.exists(imgFile)) and subprocess.call(["convert", "-density", "170", "-limit", "thread", "2", srcFile, imgFile]) != 0:
        print("error converting " + srcFile + " to " + imgFile)


def compare(imgFile1, imgFile2, diffFile):
    if subprocess.call(["compare", "-limit", "thread", "2", imgFile1, imgFile2, diffFile]) != 0:
        open(diffFile, 'a').close()


def ensureDocCompared(doc):
    with doc.lock:
        if not doc.isCompared():
            srcs = doc.srcFiles()
            imgs = doc.imgFiles()
            convert(srcs[0], imgs[0])
            convert(srcs[1], imgs[1])
            compare(imgs[0], imgs[1], imgs[2])


def worker():
    while not convertQueue.empty():
        task = convertQueue.get()
        ensureDocCompared(task.doc)
        convertQueue.task_done()


def dclick_handler(frame, doc):
    ensureDocCompared(doc)
    frame.show(doc)


parser = argparse.ArgumentParser(description="Compares images in 2 directories and browses them")
parser.add_argument("after_dir", help="directory with images after the tested change")
parser.add_argument("before_dir", help="second with images before the tested change")
#parser.add_argument("diffs_dir", default="diffs", help="resulting directory")
parser.add_argument("--file_list", default=None, help="file with list of images to compare", )
args = parser.parse_args()

Document.initDirs(args.after_dir, args.before_dir, "_picache")

docsMap={}
docKeys=[]
convertQueue = Queue.Queue()



files = None
with open(args.file_list, 'r') as f:
    files = map(lambda x: x.strip("\n")[:-4], list(f))

for l in files:
    doc = Document(l)
    docsMap[l] = doc
    docKeys.append(l)
    convertQueue.put(Task(doc))

if len(docKeys) > 0:
    if not os.path.exists(Document.cacheDir):
        os.makedirs(Document.cacheDir)
    t = Thread(target=worker)
    t.daemon = True
    t.start()

    print("Starting image browser")
    app = wx.App(False)
    frame = MyFrame(None, "Files", docKeys, docsMap, dclick_handler)
    app.MainLoop()

