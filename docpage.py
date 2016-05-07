# -*- coding: utf-8 -*-

import hashlib
import os
import os.path
import subprocess
import threading
import errno
from settings import CONVERT_CMD, COMPARE_CMD


def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _ensureConverted(src, img):
    if not os.path.exists(img):
        imgpath = os.path.dirname(img)
        if not os.path.exists(imgpath):
            _mkdir_p(imgpath)
        if subprocess.call(CONVERT_CMD + [src, img]) != 0:
            print("error converting " + src + " to " + img)
            return False
    return True


class DocPage:

    afterDir = ""
    beforeDir = ""
    cacheDir = ""

    def __init__(self, key, originalFile, diff, status=None, comment=None):
        self.key = key
        self.originalName = originalFile
        self.difference = diff
        self.status = status
        self.comment = comment
        self._lock = threading.Lock()
        self.id = hashlib.md5(self.key).hexdigest()

    @classmethod
    def initDirs(cls, afterDir, beforeDir, cacheDir ):
        cls.afterDir = afterDir
        cls.beforeDir = beforeDir
        cls.cacheDir = cacheDir

    def isCompared(self):
        return os.path.exists(self.imgDiffFilename())

    def srcBeforeFilename(self):
        return DocPage.beforeDir + "/convertedPdfFiles/" + self.key

    def srcAfterFilename(self):
        return DocPage.afterDir + "/convertedPdfFiles/" + self.key

    def imgAfterFilename(self):
        return DocPage.afterDir + "/convertedPngFiles/" + self.key + ".png"

    def imgBeforeFilename(self):
        return DocPage.beforeDir + "/convertedPngFiles/" + self.key + ".png"

    def imgDiffFilename(self):
        return DocPage.cacheDir + "/" + self.id + ".png"

    def ensureCompared(self):
        with self._lock:
            if not _ensureConverted(self.srcAfterFilename(), self.imgAfterFilename()):
                return False
            if not _ensureConverted(self.srcBeforeFilename(), self.imgBeforeFilename()):
                return False
            if not os.path.exists(self.imgDiffFilename()):
                ec = subprocess.call(COMPARE_CMD + [self.imgAfterFilename(), self.imgBeforeFilename(), self.imgDiffFilename()])
                if ec != 1:
                    print("errorcode: " + str(ec) + ". Couldn't compare " + self.imgAfterFilename() + " and " + self.imgBeforeFilename())
                    # open(self.imgDiffFilename(), 'a').close()
                    return False
        return True

    def hasStatus(self):
        return (self.status is not None) and (len(self.status) > 0)

    def hasComment(self):
        return (self.comment is not None) and (len(self.comment) > 0)

    def update(self, status, comment):
        with self._lock:
            self.status = status
            self.comment = comment
