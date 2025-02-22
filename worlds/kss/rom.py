import os
import pkgutil
import Utils
import hashlib
import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from typing import Iterable, TYPE_CHECKING, Optional
from struct import pack
from .options import subgame_mapping

if TYPE_CHECKING:
    from . import KSSWorld

KSS_UHASH = "cb76ea8ac989e71210c89102d91c6c57"
KSS_VCHASH = "5e0be1a462ffaca1351d446b96b25b74"

starting_stage = 0xAFC8C
goal_numeric = 0xAFC91
goal_specific = 0xAFC99
treasure_values = 0xAFCD1
mww_mode = 0xAFD4F


class KSSProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [KSS_UHASH, KSS_VCHASH]
    game = "Kirby Super Star"
    patch_file_ending = ".apkss"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["kss_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("calc_snes_crc", [])
    ]


    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "KSSWorld", patch: KSSProcedurePatch):
    patch.write_file("kss_basepatch.bsdiff4", pkgutil.get_data(__name__, os.path.join("data", "kss_basepatch.bsdiff4")))

    patch.write_byte(starting_stage + 1, 1 << world.options.starting_subgame.value)
    patch.write_byte(goal_numeric + 1, world.options.required_subgame_completions.value)

    required_subgames = 0
    for val, subgame in subgame_mapping.items():
        if subgame in world.options.required_subgames:
            required_subgames |= (1 << val)

    patch.write_byte(goal_specific + 1, required_subgames)
    patch.write_byte(goal_specific + 4, required_subgames)

    if world.treasure_value:
        patch.write_bytes(treasure_values, pack("IIII", *world.treasure_value))

    patch.write_byte(mww_mode + 1, world.options.milky_way_wishes_mode.value)

    patch_name = bytearray(
        f'KSS{Utils.__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch_name.extend([0] * (21 - len(patch_name)))
    patch.name = bytes(patch_name)
    patch.write_bytes(0x7FC0, patch.name)

    patch.write_file("token_patch.bin", patch.get_token_binary())


def get_base_rom_bytes() -> bytes:
    rom_file: str = get_base_rom_path()
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(Utils.read_snes_rom(open(rom_file, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {KSS_UHASH, KSS_VCHASH}:
            raise Exception("Supplied Base Rom does not match known MD5 for US or US VC release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["kss_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name