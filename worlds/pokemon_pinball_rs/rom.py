import bsdiff4
import hashlib
import os
import pkgutil
import Utils

from typing import TYPE_CHECKING, Iterable, Sequence
from worlds.Files import APProcedurePatch, APPatchExtension, APTokenMixin, APTokenTypes
from . import names
from .regions import price_functions

if TYPE_CHECKING:
    from . import PokemonPinballRSWorld

PINBALLRSHASH = "ba6d0fbff297b8937d3c8e7f2c25fa0f"

PLAYER_STRING_TABLE = 7063008
SHOP_PRICES = 7798890


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
    slot_info = 0
    if world.options.collect_pokedex:
        slot_info |= 0x1
    if world.options.ringlink:
        slot_info |= 0x2
    patch.write_byte(0x6BC024, slot_info)

    goal_value = 0
    for val in world.options.goal.value:
        if val == "Pokedex":
            goal_value |= 1
        elif val == "Score":
            goal_value |= 2
        elif val == "Targets":
            goal_value |= 4
        elif val == "Medals":
            goal_value |= 8

    targets = bytearray([0] * 26)

    for target in world.options.pokemon_targets.value:
        dexnum = names.POKEDEX[target]
        idx = dexnum // 8
        mask = dexnum % 8
        targets[idx] |= (1 << mask)

    score_low = world.options.score_requirement.value % 99999999
    score_high = world.options.score_requirement.value // 99999999

    patch.write_bytes(0x6BC030, int.to_bytes(goal_value, 2, "little"))
    patch.write_bytes(0x6BC032, int.to_bytes(world.options.pokedex_requirement.value, 2, "little"))
    patch.write_bytes(0x6BC034, int.to_bytes(score_low, 4, "little"))
    patch.write_bytes(0x6BC038, int.to_bytes(score_high, 4, "little"))
    patch.write_bytes(0x6BC03C, targets)
    patch.write_byte(0x6BC056, world.medal_goal)
    patch.write_byte(0x6BC057, world.options.goal_trigger.value)
    patch.write_byte(0x6BC058, world.options.shop_tracks.value - 1)
    patch.write_byte(0x6BC059, world.options.shop_track_length.value)
    patch.write_byte(0x6BC05A, world.options.roulette_prizes.value)
    patch.write_byte(0x6BC05B, world.options.death_link.value)

    # write our string binary here
    current_ptr = 8
    players: list[tuple[int, bytes]] = [(0, "PLAYER \x00".encode("ASCII"))]

    for idx, player in world.multiworld.player_name.items():
        if current_ptr + PLAYER_STRING_TABLE + (len(players) * 4) > PLAYER_STRING_TABLE + 0xB4000:
            # out of space in the rom
            # pop the one that went over, then break out of the loop
            players.pop()
            break
        altered_name = "".join(s for s in player.upper() if 0x20 < ord(s) < 0x5E)
        if not altered_name:
            # Name is entirely unicode, backup
            altered_name = f"PLAYER {idx}"
        altered_name += "\x00"
        players.append((current_ptr, altered_name.encode("ASCII")))
        current_ptr += len(altered_name)

    for i, (ptr, player) in enumerate(players):
        patch.write_bytes(PLAYER_STRING_TABLE + 4 + (4 * i), int.to_bytes((ptr + PLAYER_STRING_TABLE +
                                                                           (4 * len(players)) + 4) | 0x8000000,
                                                                          4, "little"))
        patch.write_bytes(PLAYER_STRING_TABLE + 4 + (4 * len(players)) + ptr, player)

    patch.write_bytes(PLAYER_STRING_TABLE, int.to_bytes(len(players) - 1, 4, "little"))

    patch.write_bytes(SHOP_PRICES, [price_functions[world.options.shop_prices.value](i) for i in range(1, 16)])

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
