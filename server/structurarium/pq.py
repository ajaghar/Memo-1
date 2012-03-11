import os
import struct
from mmap import mmap


LENGTH_LENGTH = len(struct.pack('L', 0))


class PQ(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def write(self, v):
        with open(self.file_path, 'a+b') as w:
            w.write(struct.pack('L', len(v)))
            w.write(v)

    def read(self):
        if not os.path.exists(self.file_path):
            raise StopIteration()
        file_size = os.path.getsize(self.file_path)
        with open(self.file_path, 'r+b') as w:
            i = 0
            while i < file_size:
                w.seek(i)
                size = int(struct.unpack('L', w.read(LENGTH_LENGTH))[0])
                i += LENGTH_LENGTH
                w.seek(i)
                s = w.read(size)
                yield s
                i += size
