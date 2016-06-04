"""
Input the path of a file
Return its md5
"""

import hashlib,os

def generate_md5(path):

    def read_chunks(fp):
        fp.seek(0)
        chunk = fp.read(8 * 1024)
        while chunk:
            yield chunk
            chunk = fp.read(8 * 1024)
        else:
            fp.seek(0)

    m = hashlib.md5()
    if os.path.exists(path):
        with open(path, 'rb') as fp:
            for chunk in read_chunks(fp):
                m.update(chunk)
    elif path.__class__.name__ in ["StringIO", "cStringIO"] \
            or isinstance(path, file):
        for chunk in read_chunks(path):
            m.update(chunk)
    else:
        return ""

    return m.hexdigest()

