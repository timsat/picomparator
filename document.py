# -*- coding: utf-8 -*-

import hashlib
import os
import threading

class Document:

    afterDir = ""
    beforeDir = ""
    cacheDir = ""

    IMG_AFTER = 0
    IMG_BEFORE = 1
    IMG_DIFF = 2

    SRC_AFTER = 0
    SRC_BEFORE = 1

    def __init__(self, key, originalFile, diff, status=None, comment=None):
        self.key = key
        self.originalName = originalFile
        self.difference = diff
        self.status = status
        self.comment = comment
        self.lock = threading.Lock()
        self.id = hashlib.md5(self.key).hexdigest()


    @classmethod
    def initDirs(cls, afterDir, beforeDir, cacheDir ):
        cls.afterDir = afterDir
        cls.beforeDir = beforeDir
        cls.cacheDir = cacheDir

    def isCompared(self):
        return os.path.exists(self.imgDiffFilename())

    def srcBeforeFilename(self):
        return Document.beforeDir + "/" + self.key

    def srcAfterFilename(self):
        return Document.afterDir + "/" + self.key

    def imgAfterFilename(self):
        return Document.cacheDir + "/" + self.id + "_after" + ".png"

    def imgBeforeFilename(self):
        return Document.cacheDir + "/" + self.id + "_before" + ".png"

    def imgDiffFilename(self):
        return Document.cacheDir + "/" + self.id + ".png"
