import os
import pkgutil
import Utils
import hashlib
import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from typing import Iterable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import KSSWorld

KSS_UHASH = ""

starting_stage = 0xAB86F


class KSSProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = KSS_UHASH
    game = "Kirby Super Star"
    patch_file_ending = ".apkss"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff", ["kss_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
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

    patch.write_byte(starting_stage, world.options.starting_subgame.value)

    patch_name = bytearray(
        f'KSS{Utils.__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch_name.extend([0] * (21 - len(patch_name)))
    patch.name = bytes(patch_name)
    patch.write_bytes(0x7FC0, patch.name)

def get_base_rom_bytes() -> bytes:
    rom_file: str = get_base_rom_path()
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(Utils.read_snes_rom(open(rom_file, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {KSS_UHASH}:
            raise Exception("Supplied Base Rom does not match known MD5 for US or JP release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["kdl3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name