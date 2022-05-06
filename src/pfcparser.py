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

def type_to_format_string(ftype, count = 0):
    count = int.from_bytes(count, byteorder='little')
    print(ftype, count)
    if ftype == b'\x02':
        if count > 0:
            return "{}s".format(count)
    elif ftype == b'\x04':
        return "H"
    elif ftype == b'\x06':
        return "L"

def assemble_format_string(fields):
    format_string = ""
    for f in fields:
        format_string += type_to_format_string(f[1], f[2])
    return format_string

