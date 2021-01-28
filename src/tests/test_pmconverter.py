from pmconverter import chunks, read_pfc_file, mkdirs_from_pfc_data
import os


# def test_read_data_dir(shared_datadir):
#     assert open(shared_datadir  /  "CABINFO.INI").read() == "BLAH"

def test_read_pfc_file(shared_datadir):
    pfc_filename = shared_datadir / "_PFC._PS"
    pfc_data = read_pfc_file(pfc_filename)
    assert 'TYPE' not in pfc_data
    assert 'LOCATION' not in pfc_data
    assert pfc_data[0] == ('00000002', '___system_drawer_1___')
    assert pfc_data[1] == ('00000005', 'Vegetables')

def test_chunks():
    assert [(0,1),(2,3)] == list(chunks(range(4),2))

def test_create_cabinets(tmpdir):
    pfc_data = [("000001","Vegetables"), ("000002", "Fruits")]
    output_cabinets = tmpdir.mkdir("cabinets")
    mkdirs_from_pfc_data(output_cabinets, pfc_data)
    assert "000001 - Vegetables" in list(os.listdir(output_cabinets))
    assert "000002 - Fruits" in list(os.listdir(output_cabinets))

# def test_create_dir_structure(shared_datadir,tmpdir):


"""
read cabinet data
create cabinet directories

for id in cabinets
    read folders
    make folders
     for id in folders
        read collection
        make collection folders
            for each collection
                convert tiff to pdf
                write pdf to collection folder

"""
