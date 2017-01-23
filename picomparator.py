#!/bin/python2.7
# -*- coding: utf-8 -*-

import argparse
import os.path
import string
from threading import Thread
import Queue
import locale
import wx
from frame import MyFrame
from docpage import DocPage
from settings import LOCALE
import signal
import sys


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


def worker(frame):
    while not convertQueue.empty():
        task = convertQueue.get()
        """
        @type: Task
        """
        task.doc.ensureCompared()
        convertQueue.task_done()
        wx.CallAfter(frame.RefreshDocList)


def docPageFromCsvLine(line):
    fields = line.strip('\n ').split(';')
    key = fields[0].strip('\n ')[:-4]
    diff = locale.atof(fields[1]) if len(fields) > 1 else 0.0
    status = None
    comment = None
    if len(fields) > 2:
        status = fields[2]
    if len(fields) > 3:
        comment = fields[3].decode("utf-8")
    return DocPage(key, fields[0], diff, status, comment)


def csvLineFromDocPage(docPage):
    """
    :type docPage: DocPage
    :return:
    """
    line = ';'.join([docPage.originalName, locale.str(docPage.difference), docPage.status if docPage.status is not None else ""
                        , docPage.comment if docPage.comment is not None else ""]) + "\n"
    return line.encode("utf-8")


def signal_handler(signal, frame):
    with open(args.reportfile, 'w') as f:
        f.writelines(map(csvLineFromDocPage, pages))
    sys.exit(0)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Compares images in 2 directories and browses them")
    parser.add_argument("beforedir", help="path to the images before the tested change")
    parser.add_argument("afterdir", help="path to the images after the tested change")
    parser.add_argument("reportfile", help="file with filenames and differences in CSV format e.g. differences.csv")
    args = parser.parse_args()

    locale.setlocale(locale.LC_NUMERIC, LOCALE)

    DocPage.initDirs(args.afterdir, args.beforedir, "_picache")

    convertQueue = Queue.Queue()

    signal.signal(signal.SIGINT, signal_handler)

    pages = None
    with open(args.reportfile, 'r') as f:
        pages = map(docPageFromCsvLine, filter(lambda x: len(x.strip('\n\t ')) > 0, list(f)))

    pages.sort(key=lambda x: x.key)

    for doc in pages:
        if not doc.isCompared():
            convertQueue.put(Task(doc))

    if len(pages) > 0:
        app = wx.App(False)
        frame = MyFrame(None, "Files", pages)
        if not os.path.exists(DocPage.cacheDir):
            os.makedirs(DocPage.cacheDir)
        t = Thread(target=worker, args=(frame, ))
        t.daemon = True
        t.start()

        print("Starting image browser")
        app.Bind(wx.EVT_KEY_DOWN, frame.onKeyDown)
        app.MainLoop()

        with open(args.reportfile, 'w') as f:
            f.writelines(map(csvLineFromDocPage, pages))

