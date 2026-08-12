import hashlib
import os
import pkgutil
import Utils

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from . import MM4World

MM4LCHASH = "81320c2cc7019ccbeb645a893b2cf3ec"
PROTEUSHASH = "b69fff40212b80c94f19e786d1efbf61"
MM4NESHASH = "db45eb9413964295adb8d1da961807cc"
MM4VCHASH = "92f52ebb2edf81a3659ea4b8ea0b1191"


class MM4ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [MM4LCHASH, MM4NESHASH, MM4VCHASH]
    game = "Mega Man 4"
    patch_file_ending = ".apmm4"
    result_file_ending = ".nes"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["mm4_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "MM4World", patch: MM4ProcedurePatch) -> None:
    patch.write_file("mm4_basepatch.bsdiff4", pkgutil.get_data(__name__, os.path.join("data", "mm4_basepatch.bsdiff4")))


header = b"\x4E\x45\x53\x1A\x20\x00\x40\x08\x00\x00\x00\x07\x00\x00\x00\x01"


def read_headerless_nes_rom(rom: bytes) -> bytes:
    if rom[:4] == b"NES\x1A":
        return rom[16:]
    else:
        return rom


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: bytes | None = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = read_headerless_nes_rom(bytes(open(file_name, "rb").read()))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() == PROTEUSHASH:
            base_rom_bytes = extract_mm4(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM4LCHASH, MM4NESHASH, MM4VCHASH}:
            print(basemd5.hexdigest())
            if basemd5.hexdigest() == "ab9ad69f29f812cb520dd49b39805491":
                raise Exception("Supplied Base Rom is a Rev 1 copy of Mega Man 4. Please contact the developer to "
                                "add support for this version.")
            raise Exception("Supplied Base Rom does not match known MD5 for US, LC, or US VC release. "
                            "Get the correct game and version, then dump it")
        headered_rom = bytearray(base_rom_bytes)
        headered_rom[0:0] = header
        setattr(get_base_rom_bytes, "base_rom_bytes", bytes(headered_rom))
        return bytes(headered_rom)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from . import MM4World
    if not file_name:
        file_name = MM4World.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


prg_offset = 0x12F1F0
prg_size = 0x80000


def extract_mm4(proteus: bytes) -> bytes:
    mm4 = bytearray(proteus[prg_offset:prg_offset + prg_size])
    return bytes(mm4)
