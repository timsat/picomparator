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

'''
    def __eq__(self, other):
        """
        :type other: Task
        :return:
        """
        return self.doc.key == other.doc.key

    def __cmp__(self, other):
        """
        :type other: Task
        :return:
        """
        if self.__eq__(other):
            return 0
        if self.priority == other.priority:
            raise Exception("illegal state")

        return self.priority - other.priority
'''


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
        print "error converting " + srcFile + " to " + imgFile


def compare(imgFile1, imgFile2, diffFile):
    if subprocess.call(["compare", "-limit", "thread", "2", imgFile1, imgFile2, diffFile]) != 0:
        open(diffFile, 'a').close()

parser = argparse.ArgumentParser(description="Compares images in 2 directories and browses them")
parser.add_argument("new_dir", help="directory with new images")
parser.add_argument("old_dir", help="second with old images")
#parser.add_argument("diffs_dir", default="diffs", help="resulting directory")
parser.add_argument("--file_list", default=None, help="file with list of images to compare", )
args = parser.parse_args()

Document.initDirs(args.new_dir, args.old_dir, "_picache")

docsMap={}
docKeys=[]
normalQueue = Queue.Queue()
priorityQueue = Queue.Queue()

def worker():
    while not normalQueue.empty():
        if not priorityQueue.empty():
            queue = priorityQueue
        else:
            queue = normalQueue

        task = queue.get()
        if not task.doc.isCompared():
            srcs = task.doc.srcFiles()
            imgs = task.doc.imgFiles()
            convert(srcs[0], imgs[0])
            convert(srcs[1], imgs[1])
            compare(imgs[0], imgs[1], imgs[2])
        queue.task_done()

def handler(frame, doc):
    if not doc.isCompared():
        srcs = doc.srcFiles()
        imgs = doc.imgFiles()
        convert(srcs[0], imgs[0])
        convert(srcs[1], imgs[1])
        compare(imgs[0], imgs[1], imgs[2])

    frame.show(doc)


files = None
with open(args.file_list, 'r') as f:
    files = map(lambda x: x.strip("\n")[:-4], list(f))

for l in files:
    doc = Document(l)
    docsMap[l] = doc
    docKeys.append(l)
    normalQueue.put(Task(doc))

if len(docKeys) > 0:
    if not os.path.exists(Document.cacheDir):
        os.makedirs(Document.cacheDir)
    t = Thread(target=worker)
    t.daemon = True
    t.start()

    print "Starting image browser"
    app = wx.App(False)
    frame = MyFrame(None, "Files", docKeys, docsMap, handler)
    app.MainLoop()

