#!/bin/python2.7
# -*- coding: utf-8 -*-

import subprocess
import argparse
import os.path
import string
import wx
import shutil
from threading import Thread
from frame import MyFrame
from docpage import DocPage
from settings import *
import Queue
import locale

class Task:
    def __init__(self, doc, priority=0):
        """
        :type doc: DocPage
        :type priority: int
        :return:
        """
        self.doc = doc
        # self.priority = priority


def visit_dir(arg, dirname, names):
    for fn in names:
        filepath = dirname + "/" + fn
        if os.path.isfile(filepath) and os.path.splitext(fn)[1].lower() == arg[1]:
            strip_index = string.index(filepath, "/", 1)+1
            arg[0][filepath[strip_index:]] = filepath


def visit_diffs(arg, dirname, names):
    for fn in names:
        filepath = dirname + "/" + fn
        if os.path.isfile(filepath) and os.path.splitext(fn)[1].lower() == arg[1]:
            strip_index=string.index(filepath, "/", 1)+1
            arg[0].append(filepath[strip_index:])


def convert(srcFile, imgFile):
    if not os.path.exists(srcFile + '.png'):
        if (not os.path.exists(imgFile)) and subprocess.call(CONVERT_CMD + [srcFile, imgFile]) != 0:
            print("error converting " + srcFile + " to " + imgFile)
    else:
        shutil.copy(srcFile + '.png', imgFile)


def compare(imgFile1, imgFile2, diffFile):
    if subprocess.call(COMPARE_CMD + [imgFile1, imgFile2, diffFile]) != 0:
        open(diffFile, 'a').close()


def ensureDocCompared(doc):
    """
    :type doc: DocPage
    :return:
    """
    with doc.lock:
        if not doc.isCompared():
            convert(doc.srcAfterFilename(), doc.imgAfterFilename())
            convert(doc.srcBeforeFilename(), doc.imgBeforeFilename())
            compare(doc.imgAfterFilename(), doc.imgBeforeFilename(), doc.imgDiffFilename())


def worker(frame):
    while not convertQueue.empty():
        task = convertQueue.get()
        ensureDocCompared(task.doc)
        convertQueue.task_done()
        wx.CallAfter(frame.RefreshDocList)


def dclick_handler(frame, doc):
    ensureDocCompared(doc)
    frame.show(doc)


def docFromCsvLine(line):
    fields = line.split(';')
    key = fields[0].strip('\n ')[:-4]
    diff = locale.atof(fields[1]) if len(fields) > 1 else 0.0
    status = None
    comment = None
    if len(fields) > 2:
        status = fields[2]
    if len(fields) > 3:
        comment = fields[3]
    return DocPage(key, fields[0], diff, status, comment)


parser = argparse.ArgumentParser(description="Compares images in 2 directories and browses them")
parser.add_argument("beforedir", help="path to the images before the tested change")
parser.add_argument("afterdir", help="path to the images after the tested change")
parser.add_argument("--filelist", default=None, help="file with filenames and differences in CSV format e.g. differences.csv")
args = parser.parse_args()

locale.setlocale(locale.LC_NUMERIC, 'ru_RU')

DocPage.initDirs(args.afterdir, args.beforedir, "_picache")

convertQueue = Queue.Queue()

documents = None
with open(args.filelist, 'r') as f:
    documents = map(docFromCsvLine, filter(lambda x: len(x.strip('\n\t ')) > 0, list(f)))

for doc in documents:
    convertQueue.put(Task(doc))

if len(documents) > 0:
    app = wx.App(False)
    frame = MyFrame(None, "Files", documents, dclick_handler)
    if not os.path.exists(DocPage.cacheDir):
        os.makedirs(DocPage.cacheDir)
    t = Thread(target=worker, args=(frame, ))
    t.daemon = True
    t.start()

    print("Starting image browser")
    app.Bind(wx.EVT_KEY_DOWN, frame.onKeyDown)
    app.MainLoop()

