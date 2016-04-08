# -*- coding: utf-8 -*-

import hashlib
import os

class Document:

    newDir=""
    oldDir=""
    cacheDir=""


    def __init__(self, key):
        self.key = key


    @classmethod
    def initDirs(cls, newDir, oldDir, cacheDir ):
        cls.newDir = newDir
        cls.oldDir = oldDir
        cls.cacheDir = cacheDir


    def isCompared(self):
        imgFiles = self.imgFiles()
        return os.path.exists(imgFiles[2])


    def cachedImageFile(self, dir):
        return Document.cacheDir + "/" + hashlib.md5(dir + "/" + self.key).hexdigest() + ".png"


    def srcFiles(self):
        newSrc = Document.newDir + "/" + self.key
        oldSrc = Document.newDir + "/" + self.key
        return (newSrc, oldSrc)


    def imgFiles(self):
        h = hashlib.md5(self.key).hexdigest()
        newImage  = Document.cacheDir + "/" + h + "_after" + ".png"
        oldImage  = Document.cacheDir + "/" + h + "_before" + ".png"
        diffImage = Document.cacheDir + "/" + h + ".png"
        return (newImage, oldImage, diffImage)
