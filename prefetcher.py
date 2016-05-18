# -*- coding: utf-8 -*-
import threading
from time import sleep
from collections import deque


class Prefetcher:
    def __init__(self, func, sleeptime, cachesize):
        self._queue = deque(maxlen=5)
        self._queueLock = threading.Lock()
        self._cacheLastId = -1
        self._cacheSize = cachesize
        self._cache = {}
        self._cacheLock = threading.Lock()
        self._func = func
        self._thread = threading.Thread(target=self._worker, args=(self,))
        self._isStopped = False
        self._sleeptime = sleeptime
        self._thread.start()

    def close(self):
        self._isStopped = True
        self._thread.join(2)

    def add(self, key, *args):
        with self._queueLock:
            self._queue.appendleft((key, args))

    @staticmethod
    def _worker(self):
        """
        :type self: Prefetcher
        :return:
        """
        while not self._isStopped:
            if len(self._queue) > 0:
                with self._queueLock:
                    task = self._queue.pop()
                result = self._func(*task[1])
                with self._cacheLock:
                    self._cacheLastId += 1
                    self._cache[task[0]] = (self._cacheLastId, result)
                self._prune_cache()
            else:
                sleep(self._sleeptime)

    def _prune_cache(self):
        if len(self._cache) > self._cacheSize:
            with self._cacheLock:
                for k, v in self._cache.items():
                    if v[0] <= self._cacheLastId - self._cacheSize:
                        del self._cache[k]

    def get(self, key, *args):
        self._cacheLock.acquire()
        if key not in self._cache:
            self._cacheLock.release()
            result = self._func(*args)
            self._cacheLock.acquire()
            self._cacheLastId += 1
            self._cache[key] = (self._cacheLastId, result)
            self._cacheLock.release()
            self._prune_cache()
        else:
            result = self._cache[key][1]
            self._cacheLock.release()
        return result

