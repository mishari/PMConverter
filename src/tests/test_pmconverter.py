from pmconverter import chunks, read_pfc_file, mkdirs_from_pfc_data, create_dir_structure, find_data_dirs, map_src_dir_to_dst_dir,prepare_directory_to_glob, convert_pm, get_file_extension
import os


def test_read_pfc_file(shared_datadir):
    pfc_path = shared_datadir / "_PFC._PS"
    pfc_data = read_pfc_file(pfc_path)
    assert 'TYPE' not in pfc_data
    assert 'LOCATION' not in pfc_data
    assert pfc_data[0] == ('00000002', '___system_drawer_1___')
    assert pfc_data[1] == ('00000005', 'Vegetables')

def test_read_pfc_file_with_hex_id(shared_datadir):
    pfc_path = os.path.join(shared_datadir, "00000004/00000007/0000000C", "_PFC._PS")
    pfc_data = read_pfc_file(pfc_path)
    assert ("0000000D","00000") in pfc_data

def test_chunks():
    assert [(0,1),(2,3)] == list(chunks(range(4),2))

def test_create_cabinets(tmpdir):
    pfc_data = [("000001","Vegetables"), ("000002", "Fruits")]
    output_cabinets = tmpdir.mkdir("cabinets")
    mkdirs_from_pfc_data(output_cabinets, pfc_data)
    assert "000001 - Vegetables" in list(os.listdir(output_cabinets))
    assert "000002 - Fruits" in list(os.listdir(output_cabinets))

def test_create_dir_structure(shared_datadir,tmpdir):
    src_dir = shared_datadir
    dst_dir = tmpdir
    
    fruits_dir = os.path.join(dst_dir, '00000004 - Fruits')

    create_dir_structure(src_dir, dst_dir)

    assert '00000004 - Fruits' in list(os.listdir(dst_dir))
    assert '00000006 - Citrus' in list(os.listdir(fruits_dir))

def test_find_data_dirs(shared_datadir):
    data_dirs = find_data_dirs(shared_datadir)
    assert "00000004/00000007/0000000C" in data_dirs
    assert '00000005' not in data_dirs

def test_map_src_dir_to_dst_dir(shared_datadir,tmpdir):
    src_dir = shared_datadir
    dst_dir = tmpdir

    create_dir_structure(src_dir, dst_dir)
    results = map_src_dir_to_dst_dir(shared_datadir,tmpdir)
    assert ("00000004/00000007/0000000C","00000004 - Fruits/00000007 - Berries/0000000C - January 28, 2021 10:21 AM") in results

def test_prepare_directory_to_glob():
    s = os.path.sep
    assert "01*{}02*{}03*".format(s,s) == prepare_directory_to_glob("01{}02{}03".format(s,s))
    assert "04*{}02*{}03*".format(s,s) == prepare_directory_to_glob("04{}02{}03".format(s,s))

def test_convert_pm_tiff_files(shared_datadir,tmpdir):
    src_dir = shared_datadir
    dst_dir = tmpdir

    output_rel_path = os.path.join("00000004 - Fruits","00000007 - Berries","0000000C - January 28, 2021 10:21 AM","00000.tif")

    convert_pm(src_dir, dst_dir)

    assert os.path.exists(os.path.join(dst_dir,output_rel_path))

def test_convert_pm_jpeg_files(shared_datadir,tmpdir):
    src_dir = shared_datadir
    dst_dir = tmpdir

    output_rel_path = os.path.join("00000004 - Fruits","00000007 - Berries","00000009 - Strawberry January 07, 2021 2:47 PM","00000.jpg")

    convert_pm(src_dir, dst_dir)

    assert os.path.exists(os.path.join(dst_dir,output_rel_path))

def test_get_file_extension(shared_datadir):
    assert get_file_extension(os.path.join(shared_datadir,"00000004/00000007/00000009","0000000A")) == "jpg"
    assert get_file_extension(os.path.join(shared_datadir,"00000004/00000007/0000000C","0000000D")) == "tif"
