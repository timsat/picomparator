# -*- coding: utf-8 -*-

import hashlib
import os
import threading

class Document:

    afterDir=""
    beforeDir=""
    cacheDir=""


    def __init__(self, key, originalFile, diff, status=None, comment=None):
        self.key = key
        self.originalName = originalFile
        self.diff = diff
        self.status = status
        self.comment = comment
        self.lock = threading.Lock()


    @classmethod
    def initDirs(cls, afterDir, beforeDir, cacheDir ):
        cls.afterDir = afterDir
        cls.beforeDir = beforeDir
        cls.cacheDir = cacheDir


    def isCompared(self):
        imgFiles = self.imgFiles()
        return os.path.exists(imgFiles[2])


    def srcFiles(self):
        newSrc = Document.afterDir + "/" + self.key
        oldSrc = Document.beforeDir + "/" + self.key
        return (newSrc, oldSrc)

    def id(self):
        return hashlib.md5(self.key).hexdigest()

    def imgFiles(self):
        id = self.id()
        newImage  = Document.cacheDir + "/" + id + "_after" + ".png"
        oldImage  = Document.cacheDir + "/" + id + "_before" + ".png"
        diffImage = Document.cacheDir + "/" + id + ".png"
        return (newImage, oldImage, diffImage)
