import re
import os

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i + n])

def read_pfc_file(filename):
    content = open(filename, "rb").read()
    raw_strings = [x.decode('ascii') for x in re.findall(rb"[^\x00-\x1F\x7F-\xFF]{4,}", content)]
    cabinet_data = list(chunks(raw_strings[9:],2))
    return cabinet_data

def mkdirs_from_pfc_data(parent_dir, pfc_data):
    for c in pfc_data:
        directory = "{} - {}".format(c[0], c[1])
        cabinet_dir = os.path.join(parent_dir, directory)
        os.mkdir(cabinet_dir)

