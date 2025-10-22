import hashlib
import os
import pkgutil
import settings
import Utils

from typing import Iterable, TYPE_CHECKING
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

if TYPE_CHECKING:
    from . import MM1World

MM1LCHASH = "f26a4de87f10552fde0ab93c3069d24c"
MM1NESHASH = "4de82cfceadbf1a5e693b669b1221107"
PROTEUSHASH = "b69fff40212b80c94f19e786d1efbf61"

wily_requirement = 0x1AAB4
energylink = 0x1FF69

MM1_BOSS_WEAKNESSES = {
    0: 0x1FDEE,  # Cut Man
    1: 0x1FDF6,  # Ice Man
    2: 0x1FDFE,  # Bomb Man
    3: 0x1FE06,  # Fire Man
    4: 0x1FE0F,  # Elec Man
    5: 0x1FE16,  # Guts Man
    6: 0x1FE1F,  # Yellow Devil
    7: 0x1FE26,  # Copy Robot
    8: 0x1FE2F,  # CWU 001
    9: 0x1FE36,  # Wily Machine
}


class MM1ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man"
    hash = [MM1LCHASH, MM1NESHASH]
    patch_file_ending = ".apmm1"
    result_file_ending = ".nes"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["mm1_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "MM1World", patch: MM1ProcedurePatch):
    patch.write_file("mm1_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mm1_basepatch.bsdiff4"))

    patch.write_byte(wily_requirement + 1, world.options.required_weapons.value)
    patch.write_byte(energylink + 1, world.options.energy_link.value)

    from Utils import __version__
    patch.name = bytearray(f'MM1{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0',
                           'utf8')[:16]
    patch.name.extend([0] * (16 - len(patch.name)))
    patch.write_bytes(0x1FFF0, patch.name)
    patch.write_bytes(0x1FFED, world.world_version)
    patch.write_byte(0x1FFEC, (world.options.energy_link.value << 1) + world.options.death_link.value)

    patch.write_file("token_patch.bin", patch.get_token_binary())

header = b'\x4E\x45\x53\x1A\x08\x00\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00'


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
            base_rom_bytes = extract_mm1(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM1LCHASH, MM1NESHASH}:
            print(basemd5.hexdigest())
            raise Exception("Supplied Base Rom does not match known MD5 for US or LC release. "
                            "Get the correct game and version, then dump it")
        headered_rom = bytearray(base_rom_bytes)
        headered_rom[0:0] = header
        setattr(get_base_rom_bytes, "base_rom_bytes", bytes(headered_rom))
        return bytes(headered_rom)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mm1_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


PRG_OFFSET = 0x2AF2B0
PRG_SIZE = 0x20000


def extract_mm1(proteus: bytes) -> bytes:
    mm1 = bytearray(proteus[PRG_OFFSET:PRG_OFFSET + PRG_SIZE])
    return bytes(mm1)
