# -*- coding: utf-8 -*-
from threading import Thread

import unittest
from docpage import DocPage
import time

def worker(doc, self):
    """
    :type doc: DocPage
    :return:
    """
    with doc._lock:
        self.counter += 1
        time.sleep(1)


class DocPageTest(unittest.TestCase):
    def test_lock(self):
        self.counter = 0
        docPage = DocPage("key", "origFile", 0.0)
        t1 = Thread(target=worker, args=(docPage, self))
        t2 = Thread(target=worker, args=(docPage, self))
        self.assertEqual(self.counter, 0, "incorrect initial state")
        t1.start()
        time.sleep(0.1)
        self.assertEqual(self.counter, 1)
        t2.start()
        time.sleep(0.1)
        self.assertEqual(self.counter, 1)
        t1.join()
        self.assertEqual(self.counter, 2)
        t2.join()


