import hashlib
import os
import pkgutil
import Utils

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from typing import TYPE_CHECKING, Iterable

from .color import write_palette_shuffle
from .rules import bosses
from .options import MusicShuffle

if TYPE_CHECKING:
    from . import MM4World

MM4LCHASH = "81320c2cc7019ccbeb645a893b2cf3ec"
PROTEUSHASH = "b69fff40212b80c94f19e786d1efbf61"
MM4NESHASH = "db45eb9413964295adb8d1da961807cc"
MM4VCHASH = "92f52ebb2edf81a3659ea4b8ea0b1191"

ENERGYLINK = 0x77CC2
WILY3REQ = 0x7E88C
JAMMED = 0x7BDC9

enemy_ids: dict[str, int] = {
    # these are Object IDs in the Matrixz doc
    "Taketento": 0x10,
    "Taketento (Propeller)": 0x11,
    "Tom Boy": 0x13,
    "Sasoreenu": 0x14,
    "Swallown": 0x18,
    "Coswallown": 0x19,
    "Wall Blaster": 0x1A,
    "100 Watton": 0x1B,
    "Ratton": 0x1F,
    "Kabatoncue": 0x24,
    "Escaroo": 0x2B,
    "Whopper": 0x30,
    "Haehaey": 0x33,
    "Rackaser": 0x35,
    "Dompan": 0x37,
    "Minoan": 0x3D,
    "Super Ball Machine Jr.": 0x3E,
    "Jumbig": 0x46,
    "Shield Attacker": 0x48,
    "Totem Polen": 0x4E,
    "Metall EX (Walk)": 0x50,
    "Moby": 0x52,
    "Metall EX (Jump)": 0x56,
    "Metall EX (Spin)": 0x5C,
    "M-422A": 0x5F,
    "Puyoyon": 0x61,  # check
    "Skeleton Joe": 0x62,
    "Ring Ring": 0x64,
    "Metall Swim": 0x65,
    "Skullmet": 0x69,
    "Helipon": 0x6D,
    "Gyotot": 0x70,
    "Skull Man": 0x71,
    "Ring Man": 0x75,
    "Dust Man": 0x79,
    "Dive Man": 0x7C,
    "Drill Man": 0x7E,
    "Pharaoh Man": 0x84,
    "Mothraya": 0x87,
    "Bright Man": 0x8B,
    "Toad Man": 0x8D,
    "Battonton": 0x8E,
    "Mantan": 0x91,
    "Cossack Catcher": 0x92,
    "Square Machine": 0x95,
    "Mummira": 0x9A,
    "Imorm": 0x9C,
    "Cockroach Twins": 0x9E,
    "Mono Roader": 0xA1,
    "Cockroach Twin #2": 0xA2,
    "Metall Daddy": 0xA6,
    "Gachappon": 0xA7,
    "Tako Trash": 0xAB,
    "Pakatto 24": 0xB0,
    "Up'n'Down": 0xB2,
    "Garyoby": 0xB7,
    "Wily Machine 4-1": 0xBC,
    "Wily Machine 4-2": 0xC0,
    "Wily Capsule": 0xC4,
}

enemy_weakness_ptrs: dict[int, int] = {
    0: 0x41710,
    1: 0x59710,
    2: 0x49710,
    3: 0x53710,
    4: 0x57710,
    5: 0x51710,
    6: 0x55710,
    7: 0x4F710,
    8: 0x5B710,
    9: 0x43710,
    10: 0x45710,
    11: 0x47710,
    12: 0x4B710,
}


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

    enemy_weaknesses: dict[str, dict[int, int]] = {}

    if world.options.strict_weakness or world.options.random_weakness or world.options.plando_weakness:
        # we need to write boss weaknesses
        for boss in bosses:
            enemy_weaknesses[boss] = {i: world.weapon_damage[i][bosses[boss]] for i in world.weapon_damage}

            if world.options.strict_weakness:
                extra_damage = 0
            else:
                extra_damage = world.weapon_damage[0][bosses[boss]]
            if not world.options.random_rush:
                enemy_weaknesses[boss][9] = extra_damage
                enemy_weaknesses[boss][10] = extra_damage
            enemy_weaknesses[boss][11] = extra_damage
            enemy_weaknesses[boss][12] = extra_damage
            if boss == "Cockroach Twins":
                enemy_weaknesses["Cockroach Twin #2"] = {i: world.weapon_damage[i][bosses[boss]] for i in world.weapon_damage}
                if not world.options.random_rush:
                    enemy_weaknesses["Cockroach Twin #2"][9] = extra_damage
                    enemy_weaknesses["Cockroach Twin #2"][10] = extra_damage
                enemy_weaknesses["Cockroach Twin #2"][11] = extra_damage
                enemy_weaknesses["Cockroach Twin #2"][12] = extra_damage

    if world.options.enemy_weakness:
        for enemy in enemy_ids:
            if enemy in [*bosses.keys(), "Cockroach Twin #1", "Cockroach Twin #2"]:
                continue
            enemy_weaknesses[enemy] = {weapon: world.random.randint(-4, 4) for weapon in enemy_weakness_ptrs}
            if enemy in ["Whopper", "Moby", "Escaroo", "Kabatoncue"] and enemy_weaknesses[enemy][0] <= 0:
                enemy_weaknesses[enemy][0] = 1

    for enemy, damage in enemy_weaknesses.items():
        for weapon in enemy_weakness_ptrs:
            if damage[weapon] < 0:
                damage[weapon] = 0
            patch.write_byte(enemy_weakness_ptrs[weapon] + enemy_ids[enemy], damage[weapon])

    # BUG FIX: if Cockroach Twins are defeated while Flash Stopper is active, a softlock occurs
    # This is because object 4A (the Cockroach Twins defeat handler) is marked as susceptible to Flash Stopper
    # We can just force disable this
    patch.write_byte(enemy_weakness_ptrs[1] + 0x4A, 0x00)

    patch.write_byte(WILY3REQ + 1, world.options.wily_3_requirement.value)
    patch.write_byte(ENERGYLINK + 1, world.options.energy_link.value)
    patch.write_byte(JAMMED + 1, world.options.jammed_buster.value)

    write_palette_shuffle(world, patch)

    # music shuffle
    if world.options.music_shuffle:
        if world.options.music_shuffle == MusicShuffle.option_no_music:
            pool = [0xF0] * 24
            patch.write_byte(0x36E81, 0xF0)  # intro 0A
            patch.write_byte(0x37159, 0xF0)  # intro 43
            patch.write_byte(0x6B32B, 0xF0)  # Stage Clear 0C
            patch.write_byte(0x6B7D1, 0xF0)  # Wily 4 Clear 46
            patch.write_byte(0x721C9, 0xF0)  # Cossack Castle Intro 3C
            patch.write_byte(0x7243E, 0xF0)  # Wily Castle Intro 3B
            patch.write_byte(0x72F11, 0xF0)  # Game Over 0E
            patch.write_byte(0x73061, 0xF0)  # stage intro 0F
            patch.write_byte(0x77C7C, 0xF0)  # Collect Balloon/Wire 3A
        elif world.options.music_shuffle == MusicShuffle.option_randomized:
            pool = world.random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xB, 0xD,
                                         0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x45], k=24)
        else:
            pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 1, 3, 7, 8, 9, 9, 0x15, 0x15, 0x16, 0x16, 0x10, 0x12, 0x45, 0x11, 0x0B, 0x13, 0xD, 0x14]
        world.random.shuffle(pool)
        patch.write_bytes(0x7C86B, pool[:16])
        patch.write_bytes(0x7288A, pool[16:18])  # Title Screen and Stage Select
        patch.write_byte(0x7FDB3, pool[18])  # Wily Capsule boss theme
        patch.write_byte(0x7FDBF, pool[19])  # Regular boss theme
        patch.write_byte(0x361E1, pool[20])  # Ending
        patch.write_byte(0x36375, pool[21])  # Credits
        patch.write_byte(0x72E93, pool[22])  # Password
        patch.write_byte(0x72D4C, pool[23])  # Weapon Get


    from Utils import __version__
    patch.name = bytearray(f'MM4{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0',
                           'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7EF10, patch.name)
    deathlink_byte = world.options.death_link.value | (world.options.energy_link.value << 1)
    patch.write_byte(0x7EF25, deathlink_byte)

    patch.write_bytes(0x7EF26, world.world_version)

    version_map = {
        "0": 0x18,
        "1": 0x01,
        "2": 0x02,
        "3": 0x03,
        "4": 0x04,
        "5": 0x05,
        "6": 0x06,
        "7": 0x07,
        "8": 0x08,
        "9": 0x09,
        ".": 0x24
    }

    # SILVRIS
    author = bytearray([0x1C, 0x12, 0x15, 0x1F, 0x1B, 0x12, 0x1C, 0x00])
    # ARCHIPELAGO x.x.x
    ap_version = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x0A, 0x1B, 0x0C, 0x11, 0x12, 0x19, 0x0E, 0x15, 0x0A, 0x10, 0x18, 0x00])
    ap_version.extend(list(map(lambda c: version_map[c], __version__)))
    if len(ap_version) % 2 == 1:
        ap_version.append(0)
    # just when you think you've seen it all
    group_1 = bytearray()
    group_2 = bytearray()
    for i in range(0, len(author), 2):
        group_1.append(author[i])
        group_2.append(author[i + 1])

    for i in range(0, len(ap_version), 2):
        group_1.append(ap_version[i])
        group_2.append(ap_version[i + 1])
    patch.write_bytes(0x60280, group_1)
    patch.write_bytes(0x60380, group_2)

    patch.write_file("token_patch.bin", patch.get_token_binary())


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
