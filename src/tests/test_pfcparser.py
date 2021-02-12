from pfcparser import unpack_pfc_header, read_fields

def test_read_header(shared_datadir):
    pfc_path = shared_datadir / "_PFC._PS"
    header = unpack_pfc_header(pfc_path)
    assert header[0] == 0x005344F4
    assert header[1] == 0x01234567

def test_read_num_fields(shared_datadir):
    pfc_path = shared_datadir / "_PFC._PS"
    header = unpack_pfc_header(pfc_path)
    assert header[16] == 9

def test_read_fields(shared_datadir):
    pfc_path = shared_datadir / "_PFC._PS"
    num_fields = unpack_pfc_header(pfc_path)[16]
    fields = read_fields(pfc_path, num_fields)
    assert fields[0][0] == "TYPE"

def test_read_nine_fields(shared_datadir):
    pfc_path = shared_datadir / "_PFC._PS"
    num_fields = unpack_pfc_header(pfc_path)[16]
    fields = read_fields(pfc_path, num_fields)
    assert len(fields) == 9
    
def test_last_field_is_name(shared_datadir):
    pfc_path = shared_datadir / "_PFC._PS"
    num_fields = unpack_pfc_header(pfc_path)[16]
    fields = read_fields(pfc_path, num_fields)
    assert fields[-1][0] == "NAME"

    
