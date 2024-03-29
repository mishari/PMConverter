import re
import os
import glob
import shutil
import filetype
import argparse

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i + n])

def read_pfc_file(filename):
    content = open(filename, "rb").read()
    raw_strings = [x.decode('ascii') for x in re.findall(rb"[^\x00-\x1F\x7F-\xFF]{4,}", content)]
    index = None
    for s in enumerate(raw_strings):
        if re.match("^[A-F0-9]{8}$",s[1]):
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

def map_src_dir_to_dst_dir(src_dir,dst_dir):

    dir_pairs = []

    print(dst_dir)

    for s in find_data_dirs(src_dir):
        globbed_dir = prepare_directory_to_glob(s)
        resolved_dir = glob.glob(os.path.join(dst_dir, globbed_dir))[0]
        rel_path = os.path.relpath(resolved_dir,start=dst_dir)

        dir_pairs.append((s, rel_path))

    return dir_pairs

def prepare_directory_to_glob(directory):

    globbed_dir = []
    
    for d in directory.split(os.path.sep):
        globbed_dir.append(d + "*")
    
    return os.path.sep.join(globbed_dir)

def convert_pm(src_dir, dst_dir):
    create_dir_structure(src_dir, dst_dir)
    mapped_dir = map_src_dir_to_dst_dir(src_dir,dst_dir)

    for s, d in mapped_dir:
        pfc_data = read_pfc_file(os.path.join(src_dir, s, "_PFC._PS") )
        for id, name in pfc_data:
            src_file = os.path.join(src_dir, s, id)
            print(os.path.join(dst_dir,d, name + "." + get_file_extension(src_file)))
            shutil.copyfile(src_file, os.path.join(dst_dir,d, name + "." + get_file_extension(src_file)))

def get_file_extension(filename):
    return filetype.guess(filename).extension

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adds extensions to PaperMaster files and decodes structure')
    parser.add_argument('--source', dest='src_dir', action='store',
                    help='Location of Paper Master Cabinet')
    parser.add_argument('--dest', dest='dst_dir', action='store',
                    help='Location to store converted Paper Master Cabinet')
    args = parser.parse_args()

    convert_pm(args.src_dir, args.dst_dir)


