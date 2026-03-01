# apnds/lz10.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from typing import Tuple

def decompress(data: bytes) -> bytes:
    if len(data) < 4:
        raise ValueError('cannot decompress less than 4 bytes of data')

    if data[0] != 0x10:
        raise ValueError('expected first byte of data to be decompressed to be 0x10')

    ret = bytearray(int.from_bytes(data[1:4], 'little'))

    src_pos = 4
    dest_pos = 0

    while True:
        if src_pos >= len(data):
            raise ValueError('data could not be decompressed properly')
        flags = data[src_pos]
        src_pos += 1
        for _ in range(8):
            if flags & 0x80 != 0:
                block_size = (data[src_pos] >> 4) + 3
                block_distance = (((data[src_pos] & 0xF) << 8) | data[src_pos + 1]) + 1

                src_pos += 2

                block_pos = dest_pos - block_distance
                if block_pos < 0:
                    raise ValueError('data could not be decompressed properly')

                for i in range(block_size):
                    ret[dest_pos] = ret[block_pos + i]
                    dest_pos += 1
            else:
                if src_pos >= len(data) or dest_pos >= len(ret):
                    raise ValueError('data could not be decompressed properly')
                ret[dest_pos] = data[src_pos]
                src_pos += 1
                dest_pos += 1

            if dest_pos == len(ret):
                return bytes(ret)
            flags <<= 1

def compress(data: bytes, min_distance: int = 2, forward_iteration: bool = True, pad: bool = True) -> bytes:
    if len(data) == 0:
        raise ValueError('cannot compress zero bytes')

    worst_case_dest_size = (7 + len(data) + ((len(data) + 7) // 8)) & ~3

    ret = bytearray(worst_case_dest_size)

    ret[0] = 0x10
    ret[1:4] = int.to_bytes(len(data), 3, 'little')

    src_pos = 0
    dest_pos = 4

    if forward_iteration:
        def find_best_block(src: bytes, src_pos: int) -> Tuple[int, int]:
            best_block_size = 0
            best_block_distance = 0
            block_start = max(0, src_pos - 0x1000)
            
            while block_start != src_pos:
                block_size = 0

                while block_size < 18 and src_pos + block_size < len(src) and src[block_start + block_size] == src[src_pos + block_size]:
                    block_size += 1

                if block_size > best_block_size and src_pos - block_start >= min_distance:
                    best_block_distance = src_pos - block_start
                    best_block_size = block_size

                    if block_size == 18:
                        break

                block_start += 1

            return (best_block_distance, best_block_size)
    else:
        def find_best_block(src: bytes, src_pos: int) -> Tuple[int, int]:
            best_block_size = 0
            best_block_distance = 0
            block_distance = min_distance

            while block_distance <= src_pos and block_distance <= 0x1000:
                block_start = src_pos - block_distance
                block_size = 0

                while block_size < 18 and src_pos + block_size < len(src) and src[block_start + block_size] == src[src_pos + block_size]:
                    block_size += 1

                if block_size > best_block_size:
                    best_block_distance = block_distance
                    best_block_size = block_size

                    if block_size == 18:
                        break

                block_distance += 1

            return (best_block_distance, best_block_size)

    while True:
        flags_pos = dest_pos
        dest_pos += 1
        ret[flags_pos] = 0

        for i in range(8):
            best_block_distance, best_block_size = find_best_block(data, src_pos)

            if best_block_size >= 3:
                ret[flags_pos] |= (0x80 >> i)
                src_pos += best_block_size
                best_block_size -= 3
                best_block_distance -= 1
                ret[dest_pos] = ((best_block_size << 4) | (best_block_distance >> 8)) & 0xFF
                ret[dest_pos + 1] = best_block_distance & 0xFF
                dest_pos += 2
            else:
                ret[dest_pos] = data[src_pos]
                dest_pos += 1
                src_pos += 1

            if src_pos == len(data):
                if pad:
                    rem = dest_pos & 3
                    if rem != 0:
                        for i in range(4 - rem):
                            ret[dest_pos] = 0
                            dest_pos += 1

                return bytes(ret[:dest_pos])
