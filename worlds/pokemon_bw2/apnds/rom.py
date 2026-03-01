# apnds/rom.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from collections.abc import Iterable, Mapping, MutableMapping, MutableSequence, Sequence
from dataclasses import dataclass, asdict
from enum import IntEnum
from itertools import chain
from queue import SimpleQueue
from struct import pack, pack_into, unpack_from
from typing import Literal, Tuple

BANNER_SIZE_MAP: Mapping[int, int] = {
    1: 0x840,
    2: 0x940,
    3: 0x1240,
    0x103: 0x23C0,
}

ST_MROM = 0x51E
ST_PROM = 0xD7E

TRY_CAPSHIFT_BASE = 0x20000
MAX_CAPSHIFT_PROM = 15
MAX_CAPSHIFT_MROM = 10

class HeaderField(IntEnum):
    """
    These are the fields of the header, and their corresponding offsets.
    The length of each entry is the difference of its successor's offset with it.
    """
    TITLE = 0x000
    """
    The title of the ROM. This should be null-terminated ASCII.
    """
    SERIAL = 0x00C
    MAKER = 0x010
    CHIPCAPACITY = 0x014
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    REVISION = 0x01E
    ARM9_ROMOFFSET = 0x020
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    ARM9_ENTRYPOINT = 0x024
    ARM9_LOADADDR = 0x028
    ARM9_LOADSIZE = 0x02C
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    ARM7_ROMOFFSET = 0x030
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    ARM7_ENTRYPOINT = 0x034
    ARM7_LOADADDR = 0x038
    ARM7_LOADSIZE = 0x03C
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    FNTB_ROMOFFSET = 0x040
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    FNTB_BSIZE = 0x044
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    FATB_ROMOFFSET = 0x048
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    FATB_BSIZE = 0x04C
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    OVT9_ROMOFFSET = 0x050
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    OVT9_BSIZE = 0x054
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    OVT7_ROMOFFSET = 0x058
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    OVT7_BSIZE = 0x05C
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    ROMCTRL_DEC = 0x060
    ROMCTRL_ENC = 0x064
    BANNER_ROMOFFSET = 0x068
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    SECURECRC = 0x06C
    SECURE_DELAY = 0x06E
    ARM9_AUTOLOADCB = 0x070
    ARM7_AUTOLOADCB = 0x074
    ROMSIZE = 0x080
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    HEADERSIZE = 0x084
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    STATICFOOTER = 0x088
    STATICFOOTER_END = 0x08C
    """
    This entry exists so that the STATICFOOTER entry's length is computed correctly.
    """
    HEADERCRC = 0x15E
    """
    This is computed and set automatically when converting the ROM to bytes.
    """
    HEADERCRC_END = 0x160
    """
    This entry exists so that the HEADERCRC entry's length is computed correctly.
    """
    ENTIRE_HEADER = 0x4000
    """
    This is the size of the entire header.
    """

    def succ(self) -> "HeaderField":
        """
        Given a header field, this returns the subsequent header field.
        For ENTIRE_HEADER, it returns ENTIRE_HEADER.
        """
        match self:
            case HeaderField.TITLE:
                return HeaderField.SERIAL
            case HeaderField.SERIAL:
                return HeaderField.MAKER
            case HeaderField.MAKER:
                return HeaderField.CHIPCAPACITY
            case HeaderField.CHIPCAPACITY:
                return HeaderField.REVISION
            case HeaderField.REVISION:
                return HeaderField.ARM9_ROMOFFSET
            case HeaderField.ARM9_ROMOFFSET:
                return HeaderField.ARM9_ENTRYPOINT
            case HeaderField.ARM9_ENTRYPOINT:
                return HeaderField.ARM9_LOADADDR
            case HeaderField.ARM9_LOADADDR:
                return HeaderField.ARM9_LOADSIZE
            case HeaderField.ARM9_LOADSIZE:
                return HeaderField.ARM7_ROMOFFSET
            case HeaderField.ARM7_ROMOFFSET:
                return HeaderField.ARM7_ENTRYPOINT
            case HeaderField.ARM7_ENTRYPOINT:
                return HeaderField.ARM7_LOADADDR
            case HeaderField.ARM7_LOADADDR:
                return HeaderField.ARM7_LOADSIZE
            case HeaderField.ARM7_LOADSIZE:
                return HeaderField.FNTB_ROMOFFSET
            case HeaderField.FNTB_ROMOFFSET:
                return HeaderField.FNTB_BSIZE
            case HeaderField.FNTB_BSIZE:
                return HeaderField.FATB_ROMOFFSET
            case HeaderField.FATB_ROMOFFSET:
                return HeaderField.FATB_BSIZE
            case HeaderField.FATB_BSIZE:
                return HeaderField.OVT9_ROMOFFSET
            case HeaderField.OVT9_ROMOFFSET:
                return HeaderField.OVT9_BSIZE
            case HeaderField.OVT9_BSIZE:
                return HeaderField.OVT7_ROMOFFSET
            case HeaderField.OVT7_ROMOFFSET:
                return HeaderField.OVT7_BSIZE
            case HeaderField.OVT7_BSIZE:
                return HeaderField.ROMCTRL_DEC
            case HeaderField.ROMCTRL_DEC:
                return HeaderField.ROMCTRL_ENC
            case HeaderField.ROMCTRL_ENC:
                return HeaderField.BANNER_ROMOFFSET
            case HeaderField.BANNER_ROMOFFSET:
                return HeaderField.SECURECRC
            case HeaderField.SECURECRC:
                return HeaderField.SECURE_DELAY
            case HeaderField.SECURE_DELAY:
                return HeaderField.ARM9_AUTOLOADCB
            case HeaderField.ARM9_AUTOLOADCB:
                return HeaderField.ARM7_AUTOLOADCB
            case HeaderField.ARM7_AUTOLOADCB:
                return HeaderField.ROMSIZE
            case HeaderField.ROMSIZE:
                return HeaderField.HEADERSIZE
            case HeaderField.HEADERSIZE:
                return HeaderField.STATICFOOTER
            case HeaderField.STATICFOOTER:
                return HeaderField.STATICFOOTER_END
            case HeaderField.STATICFOOTER_END:
                return HeaderField.HEADERCRC
            case HeaderField.HEADERCRC:
                return HeaderField.HEADERCRC_END
            case HeaderField.HEADERCRC_END:
                return HeaderField.ENTIRE_HEADER
            case HeaderField.ENTIRE_HEADER:
                return HeaderField.ENTIRE_HEADER

    def len(self) -> int:
        """
        This is the length of this header field, computed by `self.succ() - self`.
        """
        if self == HeaderField.ENTIRE_HEADER:
            return self
        else:
            return self.succ() - self

class Header:
    """
    This is the header of a DS ROM. Its fields can be accessed using indexing notation:
    `header[HeaderField.TITLE]` will return the title, in bytes.
    """
    data: bytearray
    """
    The underlying data of the header.
    """

    def __init__(self, data: bytes):
        """
        Initialize a header with some underlying data. The length of the data must be 0x4000 bytes.
        """
        if len(data) != HeaderField.ENTIRE_HEADER:
            raise ValueError("header data is of incorrect length (expected 0x4000 bytes)")
        self.data = bytearray(data)

    def __getitem__(self, key: HeaderField) -> bytes:
        """
        Get a field from the header as bytes.
        """
        if key == HeaderField.ENTIRE_HEADER:
            return bytes(self.data)
        else:
            return bytes(self.data[key:key.succ()])
    
    def __setitem__(self, key: HeaderField, value: bytes | int) -> None:
        """
        Set a field from the header from bytes or an integer. If an integer
        is passed, it is interpreted as little endian.
        """
        if isinstance(value, int):
            value = value.to_bytes(key.len(), 'little')
        if key == HeaderField.ENTIRE_HEADER:
            self.data[:] = value
        else:
            self.data[key:key.succ()] = value

    def get_le(self, key: HeaderField) -> int:
        """
        Get a field from the header as an integer. It is interpreted as little endian.
        """
        if key == HeaderField.ENTIRE_HEADER:
            return int.from_bytes(self.data, 'little')
        else:
            return int.from_bytes(self[key], 'little')

    def get_rom_region(self, rom: bytes, offset: HeaderField, length: HeaderField) -> bytes:
        """
        Given the entire ROM, the field corresponding to the offset in the ROM, and the
        field corresponding to the binary size in the ROM, return the region in the ROM.
        """
        off = self.get_le(offset)
        return rom[off:off + self.get_le(length)]

def get_files(header: Header, rom: bytes) -> Tuple[MutableSequence[bytes], Sequence[int]]:
    """
    Given a header and ROM, return the sequence of files in the FAT, as bytes,
    along with the order of these files within ROM.
    """
    fatb = header.get_rom_region(rom, HeaderField.FATB_ROMOFFSET, HeaderField.FATB_BSIZE)
    fatb_ints = [int.from_bytes(fatb[i:i + 4], 'little') for i in range(0, len(fatb), 4)]
    files = [rom[fatb_ints[i]:fatb_ints[i + 1]] for i in range(0, len(fatb_ints), 2)]
    order = sorted(range(len(fatb) // 8), key=lambda i : fatb_ints[2 * i])
    return (files, order)

def get_filename_id_map(fntb: bytes) -> MutableMapping[str, int]:
    """
    Given a header and ROM, return a mapping from file paths to file IDs (in the FAT).
    """

    ret = {}
    dir_queue: SimpleQueue[Tuple[int, str]] = SimpleQueue()
    # queue is (dir id, dir path)
    dir_queue.put((0, ''))

    while not dir_queue.empty():
        dir_id, dir_path = dir_queue.get()
        contents_off, file_id = unpack_from("<IH", fntb, 8 * dir_id)

        while fntb[contents_off] != 0:
            is_dir = fntb[contents_off] & 0x80 != 0
            name_len = fntb[contents_off] & 0x7F
            contents_off += 1
            path = f"{dir_path}/{fntb[contents_off:contents_off + name_len].decode('ascii')}"
            contents_off += name_len
            if is_dir:
                dir_id = 0xFFF & int.from_bytes(fntb[contents_off:contents_off + 2], 'little')
                dir_queue.put((dir_id, path))
                contents_off += 2
            else:
                ret[path] = file_id
                file_id += 1

    return ret

@dataclass
class Overlay:
    """
    This is a single overlay.
    """
    id: int
    """
    This is the overlay's ID.
    """
    ram_address: int
    """
    This is the RAM address at which the overlay is to be loaded.
    """
    ram_size: int
    """
    This is the RAM size of the overlay when loaded.
    """
    bss_size: int
    sinit_init: int
    sinit_init_end: int
    data: bytes
    """
    This is the data of the overlay.
    """
    reserved: int

def get_overlays(header: Header, rom: bytes, files: Sequence[bytes], which: Literal["9"] | Literal["7"]) -> MutableSequence[Overlay]:
    """
    Given a header, ROM, and the files in the ROM, return the overlays for either the ARM9 or ARM7 processor.
    """
    table = header.get_rom_region(rom, getattr(HeaderField, f"OVT{which}_ROMOFFSET"), getattr(HeaderField, f"OVT{which}_BSIZE"))

    ret = []

    for off in range(0, len(table), 32):
        id, ram_address, ram_size, bss_size, sinit_init, sinit_init_end, file_id, reserved = unpack_from("<8I", table, off)
        ret.append(Overlay(id, ram_address, ram_size, bss_size, sinit_init, sinit_init_end, files[file_id], reserved))

    return ret

def construct_overlay_table(overlays: Sequence[Overlay], file_id_off: int = 0) -> Tuple[bytes, Sequence[bytes]]:
    """
    Given a sequence of overlays, and a starting file ID, return the overlay table and the sequence of overlays.
    """
    table = bytes()
    data_seq = []
    for ov in overlays:
        file_id = len(data_seq) + file_id_off
        data_seq.append(ov.data)
        table_entry_data = list(asdict(ov).values())
        table_entry_data[6] = file_id
        table += pack("<8I", *table_entry_data)
    return (table, data_seq)

def path_key(path: str) -> Tuple:
    """
    The path key is the decomposition of a path `'/a/b/c'` into
    a tuple of its components, `('a', 'b', 'c')`
    """
    return tuple(path.split('/')[1:])

def path_key_to_path(*kwargs: str) -> str:
    """
    This recomposes a path from its path key.
    """
    return "/" + "/".join(kwargs)

def construct_fntb(filenames: Iterable[str], file_id_off: int) -> Tuple[bytes, Mapping[str, int]]:
    """
    Given the filenames in the ROM, and the first file ID for the files, construct the FNT
    and the mapping from filenames to file IDs.
    """
    header = bytes()
    contents = bytes()

    cur_dir = tuple()
    # path key -> dir id, seq of children (name, dir id or None)
    dir_map: MutableMapping[Tuple[str, ...], Tuple[int, MutableSequence[Tuple[str, int | None]]]] = {}
    dir_map[()] = (0xF000, [])

    def path_key_for_sorted(pk: Tuple[str, ...]) -> Tuple[str, ...]:
        return (*pk[:-1], '\0' + pk[-1])

    paths = sorted(map(path_key, filenames), key=path_key_for_sorted)

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
    filename_id_map = {}
    for pk, (_, children) in dir_map.items():
        parent_id = dir_map[pk[:-1]][0] if len(pk) > 0 else len(dir_map)
        header += pack("<I2H", len(contents) + header_len, file_id_off, parent_id)
        for name, id_if_dir in children:
            contents += int.to_bytes(len(name) | (0x00 if id_if_dir is None else 0x80), 1)
            contents += name.encode('ascii')
            if id_if_dir is not None:
                contents += int.to_bytes(id_if_dir, 2, 'little')
            else:
                filename_id_map[path_key_to_path(*pk, name)] = file_id_off
                file_id_off += 1
        contents += b'\0'

    return (header + contents, filename_id_map)

CRC_TABLE: Sequence[int] = [0, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401, 0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400]

def crc16(data: bytes, crc: int) -> int:
    """
    Compute the 16-bit CRC value for some bytes.
    """
    bit = 0

    for i in range(0, len(data), 2):
        x = int.from_bytes(data[i:i + 2], 'little')
        for bit in range(0, 16, 4):
            y = CRC_TABLE[crc & 0xF]
            crc >>= 4
            crc ^= y
            crc ^= CRC_TABLE[(x >> bit) & 0xF]

    return crc

@dataclass
class Rom:
    """
    This is the decomposition of a DS ROM into its parts.
    """
    header: Header
    """
    This is the header of the ROM.
    """
    arm9: bytes
    """
    This is the ARM9 code of the ROM.
    """
    arm7: bytes
    """
    This is the ARM7 code of the ROM.
    """
    arm9_overlays: MutableSequence[Overlay]
    """
    These are the ARM9 overlays of the ROM.
    """
    arm7_overlays: MutableSequence[Overlay]
    """
    These are the ARM7 overlays of the ROM.
    """
    files: MutableMapping[str, bytes]
    """
    This is the mapping of file paths to files in the ROM.
    """
    file_order: MutableSequence[str]
    """
    This is the physical order the files are located in the ROM, by path.
    """
    banner: bytes
    """
    This is the ROM's banner.
    """
    rom_alignment: int = 0x200
    """
    This is the alignment used starting each block when converting the ROM to bytes.
    It should be a power of two.
    """

    @staticmethod
    def from_bytes(rom: bytes) -> "Rom":
        """
        Decompose a ROM into its components.
        """
        header = Header(rom[:HeaderField.ENTIRE_HEADER])
        (file_seq, file_id_order) = get_files(header, rom)
        fntb = header.get_rom_region(rom, HeaderField.FNTB_ROMOFFSET, HeaderField.FNTB_BSIZE)
        filename_id_map = get_filename_id_map(fntb)
        arm9_ovys = get_overlays(header, rom, file_seq, "9")
        arm7_ovys = get_overlays(header, rom, file_seq, "7")
        id_filename_map = {id:name for name, id in filename_id_map.items()}
        file_order = [id_filename_map[id] for id in file_id_order if id in id_filename_map]

        arm9_start = header.get_le(HeaderField.ARM9_ROMOFFSET)
        arm9_len = header.get_le(HeaderField.ARM9_LOADSIZE)
        if arm9_start + arm9_len + 12 <= len(rom) and rom[arm9_start + arm9_len:arm9_start + arm9_len + 4] == bytes.fromhex('2106C0DE'):
            arm9_len += 12
        arm9 = rom[arm9_start:arm9_start + arm9_len]

        arm7 = header.get_rom_region(rom, HeaderField.ARM7_ROMOFFSET, HeaderField.ARM7_LOADSIZE)

        banner_off = header.get_le(HeaderField.BANNER_ROMOFFSET)
        banner_version = int.from_bytes(rom[banner_off:banner_off + 2], 'little')
        banner = rom[banner_off:banner_off + BANNER_SIZE_MAP[banner_version]]

        return Rom(header, arm9, arm7, arm9_ovys, arm7_ovys, {name:file_seq[id] for name, id in filename_id_map.items()}, file_order, banner)

    def to_bytes(self, fill_tail: bool = True, fill_with: bytes = b'\xFF') -> bytes:
        """
        From the components of a ROM, construct the ROM.
        """
        if len(fill_with) != 1:
            raise ValueError(f"fill_with has length greater than 1")

        ovt9, ovys9 = construct_overlay_table(self.arm9_overlays)
        ovt7, ovys7 = construct_overlay_table(self.arm7_overlays, len(ovys9))

        fatb = bytearray(b'\0' * (len(ovys9) + len(ovys7) + len(self.files)) * 8)
        fatb_i = 0
        post_header_bytes = bytes()
        header = Header(bytes(self.header.data))

        storage_type: Literal["MROM"] | Literal["PROM"] = "MROM" if header[HeaderField.SECURE_DELAY] == ST_MROM else "PROM"

        def cur_off() -> int:
            return len(post_header_bytes) + HeaderField.ENTIRE_HEADER
        def align_post_header_bytes() -> int:
            nonlocal post_header_bytes
            padding_len = -len(post_header_bytes) & (self.rom_alignment - 1)
            post_header_bytes += fill_with * padding_len
            return padding_len

        header[HeaderField.ARM9_ROMOFFSET] = cur_off()
        post_header_bytes += self.arm9
        align_post_header_bytes()

        if len(self.arm9) > 12 and self.arm9[-12:-8] == bytes.fromhex('2106C0DE'):
            header[HeaderField.ARM9_LOADSIZE] = len(self.arm9) - 12
        else:
            header[HeaderField.ARM9_LOADSIZE] = len(self.arm9)

        def size_after_padding(size: int) -> int:
            return size + (-size & (self.rom_alignment - 1))

        def pad_bytes(data: bytes) -> bytes:
            padding = -len(data) & (self.rom_alignment - 1)
            return data + fill_with * padding

        def write_ovs(which: Literal["9"] | Literal["7"]) -> None:
            nonlocal post_header_bytes
            nonlocal fatb_i

            ovt = ovt9 if which == "9" else ovt7
            header[getattr(HeaderField, f"OVT{which}_ROMOFFSET")] = cur_off() if len(ovt) > 0 else 0
            header[getattr(HeaderField, f"OVT{which}_BSIZE")] = len(ovt)

            post_header_bytes += ovt
            align_post_header_bytes()

            coff = cur_off()
            ovys = ovys9 if which == "9" else ovys7
            for ovy in ovys:
                pack_into("<2I", fatb, fatb_i, coff, coff + len(ovy))
                fatb_i += 8
                coff += size_after_padding(len(ovy))
            post_header_bytes += b''.join(pad_bytes(ovy) for ovy in ovys)

        write_ovs("9")

        header[HeaderField.ARM7_ROMOFFSET] = cur_off()
        post_header_bytes += self.arm7
        align_post_header_bytes()
        header[HeaderField.ARM7_LOADSIZE] = len(self.arm7)
        write_ovs("7")

        files_in_order = frozenset(self.file_order)
        file_order = list(chain(self.file_order, (filename for filename in self.files if filename not in files_in_order)))

        if len(self.files) > 0:
            (fntb, filename_id_map) = construct_fntb(self.files.keys(), len(ovys9) + len(ovys7))

            header[HeaderField.FNTB_ROMOFFSET] = cur_off()
            post_header_bytes += fntb
            align_post_header_bytes()
            header[HeaderField.FNTB_BSIZE] = len(fntb)

            file_off = cur_off() + size_after_padding(len(fatb)) + size_after_padding(len(self.banner))

            for path in file_order:
                file = self.files[path]
                pack_into("<2I", fatb, filename_id_map[path] * 8, file_off, file_off + len(file))
                file_off += size_after_padding(len(file))
        else:
            header[HeaderField.FNTB_ROMOFFSET] = 0
            header[HeaderField.FNTB_BSIZE] = 0

        header[HeaderField.FATB_ROMOFFSET] = cur_off()
        post_header_bytes += fatb
        align_post_header_bytes()
        header[HeaderField.FATB_BSIZE] = len(fatb)

        header[HeaderField.BANNER_ROMOFFSET] = cur_off()
        post_header_bytes += self.banner
        last_padding = align_post_header_bytes()

        post_header_bytes += b''.join(pad_bytes(self.files[path]) for path in file_order)

        if len(file_order) > 0:
            last_padding = -len(self.files[file_order[-1]]) & (self.rom_alignment - 1)

        if last_padding > 0:
            post_header_bytes = post_header_bytes[:-last_padding]

        rom_size = cur_off()

        trycap = TRY_CAPSHIFT_BASE
        maxshift = MAX_CAPSHIFT_PROM if storage_type == "PROM" else MAX_CAPSHIFT_MROM
        for shift in range(maxshift):
            if rom_size < (trycap << shift):
                header[HeaderField.CHIPCAPACITY] = shift
                break
        else:
            shift = maxshift
        if shift == maxshift:
            raise RuntimeError("rom size is too big")

        tailsize = trycap << shift

        header[HeaderField.ROMSIZE] = rom_size
        header[HeaderField.HEADERSIZE] = HeaderField.ENTIRE_HEADER

        header[HeaderField.HEADERCRC] = crc16(bytes(header.data[:HeaderField.HEADERCRC]), 0xFFFF)

        if fill_tail:
            post_header_bytes += fill_with * (tailsize - len(post_header_bytes) - HeaderField.ENTIRE_HEADER)

        return bytes(header.data + post_header_bytes)

__all__: list[str] = ['HeaderField', 'Header', 'Overlay', 'Rom']
