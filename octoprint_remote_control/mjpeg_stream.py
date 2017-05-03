# coding=utf-8
from __future__ import absolute_import
from Queue import Queue
from threading import Thread
import requests
import StringIO

#from octoprint import settings

def produce(q):
    #settings.get(["webcam", "stream"])
    #res = requests.get('http://localhost:8080/?action=stream&1491831111684', stream=True).raw
    res = requests.get('https://play.na7kr.us/webcam/?action=stream&1489847105132', stream=True).raw
    data = res.readline()

    chunker = MjpegStreamChunker(q)

    while(data):
        chunker.addLine(data)
        data = res.readline()

class MjpegStreamChunker:

    def __init__(self, q):
        self.q = q
        self.boundary = None
        self.current_chunk = StringIO.StringIO()

    def addLine(self, line):
        if not self.boundary:   # The first time addLine should be called with 'boundary' text as input
            self.boundary = line

        if line == self.boundary:  # start of next chunk
            q.put(self.current_chunk.getvalue())
            self.current_chunk = StringIO.StringIO()

        self.current_chunk.write(line)


if __name__ == "__main__":
    q = Queue()
    producer = Thread(target=produce, args=(q,))
    producer.start()
    with open("/tmp/test.out", 'w') as f:
        while True:
            last_chunk = ""
            while not q.empty():
                last_chunk = q.get_nowait()
            f.write(last_chunk)
            import time
            time.sleep(1)
            f.flush()

