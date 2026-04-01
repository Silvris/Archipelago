import bsdiff4
import hashlib
import os
import pkgutil
import Utils

from typing import TYPE_CHECKING, Iterable, Sequence
from worlds.Files import APProcedurePatch, APPatchExtension, APTokenMixin, APTokenTypes
from . import names

if TYPE_CHECKING:
    from . import PokemonPinballRSWorld

PINBALLRSHASH = "ba6d0fbff297b8937d3c8e7f2c25fa0f"


class RomData:
    def __init__(self, file: bytes, name: str = "") -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytearray:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values: Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str) -> None:
        with open(file, 'wb') as outfile:
            outfile.write(self.file)


class PinballRSPatchExtension(APPatchExtension):
    game = "Pokemon Pinball Ruby & Sapphire"

    @staticmethod
    def apply_basepatch(_: APProcedurePatch, rom: bytes) -> bytes:
        return bsdiff4.patch(rom, pkgutil.get_data(__name__, os.path.join("data", "pinballrs_basepatch.bsdiff4")))


class PinballRSProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = PINBALLRSHASH
    game = "Pokemon Pinball Ruby & Sapphire"
    patch_file_ending = ".appbrs"
    result_file_ending = ".gba"
    name: bytearray
    procedure = [
        ("apply_basepatch", []),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "PokemonPinballRSWorld", patch: PinballRSProcedurePatch) -> None:
    from Utils import __version__
    patch.name = bytearray(f'PBRS{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:22}\0',
                           'utf8')[:32]
    patch.name.extend([0] * (32 - len(patch.name)))
    patch.write_bytes(0x6BC000, patch.name)
    patch.write_bytes(0x6BC020, world.world_version)

    goal_value = 0
    for val in world.options.goal.value:
        if val == "Pokedex":
            goal_value |= 1
        elif val == "Score":
            goal_value |= 2
        elif val == "Targets":
            goal_value |= 4

    targets = bytearray([0] * 26)

    for target in world.options.pokemon_targets.value:
        dexnum = names.POKEDEX[target]
        idx = dexnum // 8
        mask = dexnum % 8
        targets[idx] |= (1 << mask)

    patch.write_byte(0x6BC030, goal_value)
    patch.write_byte(0x6BC031, world.options.pokedex_requirement.value)
    patch.write_bytes(0x6BC032, int.to_bytes(world.options.score_requirement.value, 8, "little"))
    patch.write_bytes(0x6BC03A, targets)

    patch.write_file("token_patch.bin", patch.get_token_binary())


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: bytes | None = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() != PINBALLRSHASH:
            print(basemd5.hexdigest())
            raise Exception("Supplied Base Rom does not match known MD5 for US, LC, or US VC release. "
                            "Get the correct game and version, then dump it")

        setattr(get_base_rom_bytes, "base_rom_bytes", bytes(base_rom_bytes))
        return base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from . import PokemonPinballRSWorld
    if not file_name:
        file_name = PokemonPinballRSWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
