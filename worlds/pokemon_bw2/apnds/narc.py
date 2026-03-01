# apnds/narc.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from .rom import get_filename_id_map, path_key_to_path, path_key

from collections.abc import Mapping, MutableMapping, MutableSequence
from dataclasses import dataclass
from struct import pack, pack_into, unpack_from
from typing import Tuple

HEADER_MAGIC = 0x4352414E
HEADER_LE_BOM = 0xFFFE
HEADER_VERSION_MARKER = 0x100

def construct_fntb_forced_ids(filename_id_map: Mapping[str, int]) -> bytes:
    header = bytes()
    contents = bytes()

    cur_dir = tuple()
    dir_map: MutableMapping[Tuple[str, ...], Tuple[int, MutableSequence[Tuple[str, int | None]]]] = {}
    dir_map[()] = (0xF000, [])

    # within a directory, this will sort files by their id.
    def path_key_for_sorted(pk: Tuple[str, ...]) -> Tuple[str, ...]:
        return (*pk[:-1], f"\0{filename_id_map[path_key_to_path(*pk)]:04X}")

    paths = sorted(map(path_key, filename_id_map), key=path_key_for_sorted)

    for pk in paths:
        parent_dir = pk[:-1]
        for i, (l, r) in enumerate(zip(cur_dir, parent_dir)):
            if l != r:
                break
        else:
            i = min(len(cur_dir), len(parent_dir))
        for j in range(i + 1, len(parent_dir) + 1):
            dir_map[parent_dir[:j - 1]][1].append((parent_dir[j - 1], len(dir_map) | 0xF000))
            dir_map[parent_dir[:j]] = (len(dir_map) | 0xF000, [])
        cur_dir = parent_dir
        dir_map[parent_dir][1].append((pk[-1], None))

    header_len = len(dir_map) * 8
    for pk, (_, children) in dir_map.items():
        parent_id = dir_map[pk[:-1]][0] if len(pk) > 0 else len(dir_map)
        base_file_id = 0
        last_file_id = None
        len_contents_before = len(contents)
        for name, id_if_dir in children:
            contents += int.to_bytes(len(name) | (0x00 if id_if_dir is None else 0x80), 1)
            contents += name.encode('ascii')
            if id_if_dir is not None:
                contents += int.to_bytes(id_if_dir, 2, 'little')
            else:
                if last_file_id is None:
                    base_file_id = last_file_id = filename_id_map[path_key_to_path(*pk, name)]
                else:
                    this_file_id = filename_id_map[path_key_to_path(*pk, name)]
                    if this_file_id != last_file_id + 1:
                        raise ValueError("canont build fnt: nonconsecutive file ids within a directory (" + path_key_to_path(*pk, name) + ")")
                    last_file_id = this_file_id
        header += pack("<I2H", len_contents_before + header_len, base_file_id, parent_id)
        contents += b'\0'

    return header + contents

@dataclass
class Narc:
    files: MutableSequence[bytes]
    filename_id_map: MutableMapping[str, int]

    @staticmethod
    def from_bytes(data: bytes) -> "Narc":
        magic, bom, version, size, header_size = unpack_from("<IHHIH", data, 0)
        
        if magic != HEADER_MAGIC:
            raise ValueError("data is not valid NARC. magic does not match")
        if bom != HEADER_LE_BOM:
            raise ValueError("data is not valid NARC. bom does not match")
        if version != HEADER_VERSION_MARKER:
            raise ValueError("data is not valid NARC. version does not match")
        if size != len(data):
            raise ValueError("data is not valid NARC. size does not match")

        fatb_pos = header_size
        if data[fatb_pos:fatb_pos + 4] != b'BTAF':
            raise ValueError("data is not valid NARC. FATB magic does not match")
        fatb_length, num_file_entries = unpack_from("<2I", data, fatb_pos + 4)
        fatb_ints = unpack_from(f"<{num_file_entries * 2}I", data, fatb_pos + 12)

        fntb_pos = fatb_pos + fatb_length
        if data[fntb_pos:fntb_pos + 4] != b'BTNF':
            raise ValueError("data is not valid NARC. FNTB magic does not match")
        fntb_len, = unpack_from("<I", data, fntb_pos + 4)

        fimg_pos = fntb_pos + fntb_len
        if data[fimg_pos:fimg_pos + 4] != b'GMIF':
            raise ValueError("data is not valid NARC. FING magic does not match")
        off = fimg_pos + 8

        file_data = data[off:]

        files = [file_data[fatb_ints[i]:fatb_ints[i + 1]] for i in range(0, 2 * num_file_entries, 2)]
        filename_id_map = get_filename_id_map(data[fntb_pos + 8:fntb_pos + fntb_len])

        return Narc(files, filename_id_map)

    def to_bytes(self) -> bytes:
        fatb_contents = bytearray(8 * len(self.files))
        coff = 0
        for i, file in enumerate(self.files):
            pack_into("<2I", fatb_contents, 8 * i, coff, coff + len(file))
            coff += len(file)
            coff += -coff & 3
        fatb = pack("<4sII", b'BTAF', 12 + 8 * len(self.files), len(self.files)) + fatb_contents
        def padded_file(file: bytes) -> bytes:
            return file + b'\0' * (-len(file) & 3)
        fimg = pack("<4sI", b'GMIF', coff + 8) + b''.join(padded_file(file) for file in self.files)
        fntb = construct_fntb_forced_ids(self.filename_id_map)
        fntb = pack("<4sI", b'BTNF', 8 + len(fntb)) + fntb

        post_header = fatb + fntb + fimg

        header = pack("<IHHIHH", HEADER_MAGIC, HEADER_LE_BOM, HEADER_VERSION_MARKER, 0x10 + len(post_header), 0x10, 3)

        return header + post_header

__all__: list[str] = ["Narc"]
