# -*- coding: utf-8 -*-

import hashlib
import os
import threading

class Document:

    newDir=""
    oldDir=""
    cacheDir=""


    def __init__(self, key):
        self.key = key
        self.lock = threading.Lock()


    @classmethod
    def initDirs(cls, newDir, oldDir, cacheDir ):
        cls.newDir = newDir
        cls.oldDir = oldDir
        cls.cacheDir = cacheDir


    def isCompared(self):
        imgFiles = self.imgFiles()
        return os.path.exists(imgFiles[2])


    def srcFiles(self):
        newSrc = Document.newDir + "/" + self.key
        oldSrc = Document.oldDir + "/" + self.key
        return (newSrc, oldSrc)

    def id(self):
        return hashlib.md5(self.key).hexdigest()

    def imgFiles(self):
        id = self.id()
        newImage  = Document.cacheDir + "/" + id + "_after" + ".png"
        oldImage  = Document.cacheDir + "/" + id + "_before" + ".png"
        diffImage = Document.cacheDir + "/" + id + ".png"
        return (newImage, oldImage, diffImage)
