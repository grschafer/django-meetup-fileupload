# -*- coding: utf-8 -*-
import argparse
from filechunkio import FileChunkIO
import requests
import os
import math

UPLOAD_URL = 'http://10.1.10.242:8000/chunked/'
UPLOAD_URL_NOCHUNK = 'http://10.1.10.242:8000/minimal/'
CHUNK_SIZE = 5 * 1024 * 1024 # 5 mb chunk

class Chunk(object):
    def __init__(self, index, offset, bytes):
        self.index = index
        self.offset = offset
        self.bytes = bytes

def gen_chunks(num_chunks, filesize, missing_chunks=None):
    make_chunks = missing_chunks or range(num_chunks)
    for index in make_chunks:
        offset = index * CHUNK_SIZE
        remaining_bytes = filesize - offset
        bytes = min(CHUNK_SIZE, remaining_bytes)
        yield Chunk(index, offset, bytes)

def upload_file(filepath):
    # TODO: issues with identifying based on filename
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    num_chunks = math.ceil(filesize / float(CHUNK_SIZE))
    missing_chunks = None
    resp = requests.get(UPLOAD_URL, params={'filename': filename})

    if resp.ok:
        print('Resuming existing upload:', filepath)
        missing_chunks = resp.json()['missing_chunks']
    else:
        print('Starting new upload:', filepath)
        print(requests.post(UPLOAD_URL, params={'filename': filename}, data={
            'filesize': filesize,
            'num_chunks': num_chunks,
            'chunk_size': CHUNK_SIZE,
            }))

    for chunk in gen_chunks(num_chunks, filesize, missing_chunks):
        print('sending chunk', chunk.index, chunk.offset, chunk.bytes)
        with FileChunkIO(filepath, 'rb', offset=chunk.offset, bytes=chunk.bytes) as fin:
            metadata = {
                    'index': chunk.index,
                    'size': chunk.bytes,
                    }
            files = {'file': fin}
            print(requests.post(UPLOAD_URL, params={'filename': filename}, data=metadata, files=files))
        # NOTE: uncomment the break to upload 1 chunk at a time (resumable)
        #break

import time
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to file to upload')
    parser.add_argument('-n', '--not-chunked',
            default=False,
            action='store_true',
            help='Use simple upload instead of chunked')
    args = parser.parse_args()

    if args.not_chunked:
        print('Using simple upload scheme')
        start = time.time()
        with open(args.path, 'rb') as fin:
            requests.post(UPLOAD_URL_NOCHUNK, files={'file': fin})
        end = time.time()
    else:
        print('Using chunked upload scheme')
        start = time.time()
        upload_file(args.path)
        end = time.time()
    print('Took', end - start, 'seconds')
