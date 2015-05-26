# TODO: implement client
# param: file
# POST
# chop it up with filechunkio
# PUT each piece (in parallel)
import argparse
from filechunkio import FileChunkIO
import requests
import os
import math

UPLOAD_URL = 'http://192.168.1.231:8000/chunked/'
CHUNK_SIZE = 5

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
        # TODO: jump to PUTs (only for missing chunks)
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
        break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to file to upload')
    args = parser.parse_args()
    upload_file(args.path)
