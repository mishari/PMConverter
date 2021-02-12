# PFC Parser is a port of http://www.verycomputer.com/49_fe29cab9ff071569_1.htm
import struct

def unpack_pfc_header(pfc_path):
    header = struct.unpack("<15L2H", open(pfc_path,'rb').read(64))
    return header

def read_fields(pfc_path, num_fields):
    f = open(pfc_path,'rb')
    _ = f.seek(64)
    fields = []
    for _ in range(num_fields):
        raw_row = f.read(32)
        row_data = struct.unpack("<28sccH", raw_row)
        cleaned_row_data = [r for r in row_data]
        cleaned_row_data[0] = cleaned_row_data[0].decode('ascii').strip('\0')
        fields.append(cleaned_row_data)
    return fields