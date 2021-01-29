import re
import os

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i + n])

def read_pfc_file(filename):
    content = open(filename, "rb").read()
    raw_strings = [x.decode('ascii') for x in re.findall(rb"[^\x00-\x1F\x7F-\xFF]{4,}", content)]
    index = None
    for s in enumerate(raw_strings):
        if s[1].isdigit():
            index = s[0]
            break
    if index == None:
        cabinet_data = []
    else:
        cabinet_data = list(chunks(raw_strings[index:],2))
    return cabinet_data

def mkdirs_from_pfc_data(parent_dir, pfc_data):
    for c in pfc_data:
        try:
            directory = "{} - {}".format(c[0], c[1])
            cabinet_dir = os.path.join(parent_dir, directory)
            os.mkdir(cabinet_dir)
        except IndexError:
            pass

def create_dir_structure(src_dir,dst_dir):

    if os.path.exists(os.path.join(src_dir, "_PFC._PS")):
        pfc_data = read_pfc_file(os.path.join(src_dir, "_PFC._PS"))
    else:
        return
    
    if pfc_data == []:
        return

    mkdirs_from_pfc_data(dst_dir, pfc_data)

    for d in pfc_data:
        try:
            create_dir_structure(os.path.join(src_dir, d[0]), os.path.join(dst_dir, "{} - {}".format(d[0], d[1])))
        except IndexError:
            pass

def find_data_dirs(src_dir):

    data_dirs = []

    for root, _, _ in os.walk(src_dir, topdown=True):
        rel_path = os.path.relpath(root,start=src_dir)
        if rel_path.count(os.sep) == 2:
            data_dirs.append(rel_path)
    return data_dirs