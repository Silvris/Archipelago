from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict

BLOCK_ORDERS: dict[int, str] = {
    0: "ABCD",
    1: "ABDC",
    2: "ACBD",
    3: "ACDB",
    4: "ADBC",
    5: "ADCB",
    6: "BACD",
    7: "BADC",
    8: "BCAD",
    9: "BCDA",
    10: "BDAC",
    11: "BDCA",
    12: "CABD",
    13: "CADB",
    14: "CBAD",
    15: "CBDA",
    16: "CDAB",
    17: "CDBA",
    18: "DABC",
    19: "DACB",
    20: "DBAC",
    21: "DBCA",
    22: "DCAB",
    23: "DCBA",
}

PBR_ENCODING: defaultdict[str, int] = defaultdict(lambda: 0x00E0, {
    **{str(num): 0x0121 + num for num in range(10)},
    **{capital: 0x012B + i for i, capital in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")},
    **{lowercase: 0x0145 + i for i, lowercase in enumerate("abcdefghijklmnopqrstuvwxyz")},
    ",": 0x01AD,
    ".": 0x01AE,
    "/": 0x01B1,
    "'": 0x01B3,
    "-": 0x01BE,
    " ": 0x01DE,
    # add more as needed/wanted
})

PBR_ENCODING_INVERSE: dict[int, str] = {value: key for key, value in PBR_ENCODING.items()}

BLOCK_SIZE = 0x20

@dataclass
class Gen4Pokemon:
    personality_value: int = 0 # int
    flagsBase: int = 0 # half
    checksum: int = 0 # half

    # Block A
    species: int = 0 # half
    held_item: int = 0 # half
    tid: int = 0 # half
    sid: int = 0 # half
    experience: int = 0 # int
    friendship: int = 0 # byte
    ability: int = 0 # byte
    markings: int = 0 # byte
    language: int = 0 # byte
    hp_ev: int = 0 # byte
    atk_ev: int = 0 # byte
    def_ev: int = 0 # byte
    spe_ev: int = 0 # byte
    spa_ev: int = 0 # byte
    spd_ev: int = 0 # byte
    cool: int = 0 # byte
    beauty: int = 0 # byte
    cute: int = 0 # byte
    smart: int = 0 # byte
    tough: int = 0 # byte
    sheen: int = 0 # byte
    sinnoh_ribbons_1: int = 0 # int

    # Block B
    move1: int = 0 # half
    move2: int = 0 # half
    move3: int = 0 # half
    move4: int = 0 # half
    move1_pp: int = 0 # byte
    move2_pp: int = 0 # byte
    move3_pp: int = 0 # byte
    move4_pp: int = 0 # byte
    ppup_1: int = 0 # byte
    ppup_2: int = 0 # byte
    ppup_3: int = 0 # byte
    ppup_4: int = 0 # byte
    ivs: int = 0 # int, top two bits are flags
    hoenn_ribbons: int = 0 # int
    flagsB: int = 0 # half, fateful/gender/forme/shiny crown
    unusedB: int = 0 # half
    plat_egg_loc: int = 0 # half
    plat_met_loc: int = 0 # half

    # Block C
    nickname: str = "" # 10 halfs + 0xFFFF terminator
    unusedC1: int = 0 # byte
    game_of_origin: int = 0 # byte
    sinnoh_ribbons_2: int = 0 # int
    unusedC2: int = 0 # int

    # Block D
    trainer_name: str = "" # 16 bytes total including an FF terminator
    egg_date_1: int = 0 # byte
    egg_date_2: int = 0 # byte
    egg_date_3: int = 0 # byte
    met_date_1: int = 0 # byte
    met_date_2: int = 0 # byte
    met_date_3: int = 0 # byte
    dp_egg_loc: int = 0 # half
    dp_met_loc: int = 0 # half
    pokerus: int = 0 # byte
    pokeball: int = 0 # byte
    met_level: int = 0 # byte, top bit is OT gender
    encounter_type: int = 0 # byte
    hgss_pokeball: int = 0 # byte
    mood: int = 0 # byte

    def parse_a_block(self, data: bytes) -> None:
        self.species = int.from_bytes(data[0:2], byteorder="big")
        self.held_item = int.from_bytes(data[2:4], byteorder="big")
        self.tid = int.from_bytes(data[4:6], byteorder="big")
        self.sid = int.from_bytes(data[6:8], byteorder="big")
        self.experience = int.from_bytes(data[8:0xC], byteorder="big")
        self.friendship = data[0xC]
        self.ability = data[0xD]
        self.markings = data[0xE]
        self.language = data[0xF]
        self.hp_ev = data[0x10]
        self.atk_ev = data[0x11]
        self.def_ev = data[0x12]
        self.spe_ev = data[0x13]
        self.spa_ev = data[0x14]
        self.spd_ev = data[0x15]
        self.cool = data[0x16]
        self.beauty = data[0x17]
        self.cute = data[0x18]
        self.smart = data[0x19]
        self.tough = data[0x1A]
        self.sheen = data[0x1B]
        self.sinnoh_ribbons_1 = int.from_bytes(data[0x1C:0x20], byteorder="big")

    def build_a_block(self) -> bytes:
        output = bytearray()
        output.extend(self.species.to_bytes(2, byteorder="big"))
        output.extend(self.held_item.to_bytes(2, byteorder="big"))
        output.extend(self.tid.to_bytes(2, byteorder="big"))
        output.extend(self.sid.to_bytes(2, byteorder="big"))
        output.extend(self.experience.to_bytes(4, byteorder="big"))
        output.append(self.friendship)
        output.append(self.ability)
        output.append(self.markings)
        output.append(self.language)
        output.append(self.hp_ev)
        output.append(self.atk_ev)
        output.append(self.def_ev)
        output.append(self.spe_ev)
        output.append(self.spa_ev)
        output.append(self.spd_ev)
        output.append(self.cool)
        output.append(self.beauty)
        output.append(self.cute)
        output.append(self.smart)
        output.append(self.tough)
        output.append(self.sheen)
        output.extend(self.sinnoh_ribbons_1.to_bytes(4, byteorder="big"))

        return bytes(output)

    def parse_b_block(self, data: bytes) -> None:
        self.move1 = int.from_bytes(data[0x0:0x2], byteorder="big")
        self.move2 = int.from_bytes(data[0x2:0x4], byteorder="big")
        self.move3 = int.from_bytes(data[0x4:0x6], byteorder="big")
        self.move4 = int.from_bytes(data[0x6:0x8], byteorder="big")
        self.move1_pp = data[8]
        self.move2_pp = data[9]
        self.move3_pp = data[0xA]
        self.move4_pp = data[0xB]
        self.ppup_1 = data[0xC]
        self.ppup_2 = data[0xD]
        self.ppup_3 = data[0xE]
        self.ppup_4 = data[0xF]
        self.ivs = int.from_bytes(data[0x10:0x14], byteorder="big")
        self.hoenn_ribbons = int.from_bytes(data[0x14:0x18], byteorder="big")
        self.flagsB = int.from_bytes(data[0x18:0x1A], byteorder="big")
        self.unusedB = int.from_bytes(data[0x1A:0x1C], byteorder="big")
        self.plat_egg_loc = int.from_bytes(data[0x1C:0x1E], byteorder="big")
        self.plat_met_loc = int.from_bytes(data[0x1E:0x20], byteorder="big")

    def build_b_block(self) -> bytes:
        output = bytearray()
        output.extend(self.move1.to_bytes(2, byteorder="big"))
        output.extend(self.move2.to_bytes(2, byteorder="big"))
        output.extend(self.move3.to_bytes(2, byteorder="big"))
        output.extend(self.move4.to_bytes(2, byteorder="big"))
        output.append(self.move1_pp)
        output.append(self.move2_pp)
        output.append(self.move3_pp)
        output.append(self.move4_pp)
        output.append(self.ppup_1)
        output.append(self.ppup_2)
        output.append(self.ppup_3)
        output.append(self.ppup_4)
        output.extend(self.ivs.to_bytes(4, byteorder="big"))
        output.extend(self.hoenn_ribbons.to_bytes(4, byteorder="big"))
        output.extend(self.flagsB.to_bytes(2, byteorder="big"))
        output.extend(self.unusedB.to_bytes(2, byteorder="big"))
        output.extend(self.plat_egg_loc.to_bytes(2, byteorder="big"))
        output.extend(self.plat_met_loc.to_bytes(2, byteorder="big"))

        return bytes(output)

    def parse_c_block(self, data: bytes) -> None:
        nickname_bytes = data[:0x16]
        nickname = ""
        for i in range(11):
            char = int.from_bytes(nickname_bytes[(i*2):(i*2)+2], byteorder="big")
            if char == 0xFFFF or char == 0x00:
                break
            nickname += PBR_ENCODING_INVERSE[char]
        self.nickname = nickname
        self.unusedC1 = data[0x16]
        self.game_of_origin = data[0x17]
        self.sinnoh_ribbons_2 = int.from_bytes(data[0x18:0x1C], byteorder="big")
        self.unusedC2 = int.from_bytes(data[0x1C:0x20], byteorder="big")

    def build_c_block(self) -> bytes:
        nickname = self.nickname[:10] # trim nickname past 10 characters
        output = bytearray()
        for char in nickname:
            output.extend(PBR_ENCODING[char].to_bytes(2, byteorder="big"))
        output.extend([0xFF, 0xFF])
        output.extend([0] * ((10 - len(nickname)) * 2))
        output.append(self.unusedC1)
        output.append(self.game_of_origin)
        output.extend(self.sinnoh_ribbons_2.to_bytes(4, byteorder="big"))
        output.extend(self.unusedC2.to_bytes(4, byteorder="big"))

        return bytes(output)

    def parse_d_block(self, data: bytes) -> None:
        trainer_bytes = data[:0x10]
        trainer = ""
        for i in range(8):
            char = int.from_bytes(trainer_bytes[(i*2):(i*2)+2], byteorder="big")
            if char == 0xFFFF or char == 0x0000:
                break
            trainer += PBR_ENCODING_INVERSE[char]
        self.trainer_name = trainer
        self.egg_date_1 = data[0x10]
        self.egg_date_2 = data[0x11]
        self.egg_date_3 = data[0x12]
        self.met_date_1 = data[0x13]
        self.met_date_2 = data[0x14]
        self.met_date_3 = data[0x15]
        self.dp_egg_loc = int.from_bytes(data[0x16:0x18], byteorder="big")
        self.dp_met_loc = int.from_bytes(data[0x18:0x1A], byteorder="big")
        self.pokerus = data[0x1A]
        self.pokeball = data[0x1B]
        self.met_level = data[0x1C]
        self.encounter_type = data[0x1D]
        self.hgss_pokeball = data[0x1E]
        self.mood = data[0x1F]

    def build_d_block(self) -> bytes:
        trainer_name = self.trainer_name[:7]
        output = bytearray()
        for char in trainer_name:
            output.extend(PBR_ENCODING[char].to_bytes(2, byteorder="big"))
        output.extend([0xFF, 0xFF])
        output.extend([0] * ((7 - len(trainer_name)) * 2))
        output.append(self.egg_date_1)
        output.append(self.egg_date_2)
        output.append(self.egg_date_3)
        output.append(self.met_date_1)
        output.append(self.met_date_2)
        output.append(self.met_date_3)
        output.extend(self.dp_egg_loc.to_bytes(2, byteorder="big"))
        output.extend(self.dp_met_loc.to_bytes(2, byteorder="big"))
        output.append(self.pokerus)
        output.append(self.pokeball)
        output.append(self.met_level)
        output.append(self.encounter_type)
        output.append(self.hgss_pokeball)
        output.append(self.mood)

        return bytes(output)

    @classmethod
    def create_from_binary(cls, data: bytes) -> Gen4Pokemon:
        mon = Gen4Pokemon()
        mon.personality_value = int.from_bytes(data[0x0:0x4], byteorder="big")
        mon.flagsBase = int.from_bytes(data[0x4:0x6], byteorder="big")
        mon.checksum = int.from_bytes(data[0x6:0x8], byteorder="big")

        block_functions = {
            "A": mon.parse_a_block,
            "B": mon.parse_b_block,
            "C": mon.parse_c_block,
            "D": mon.parse_d_block,
        }

        blocks = [data[0x8 + (i*0x20):0x28 + (0x20*i)] for i in range(4)]
        block_shuffle = BLOCK_ORDERS[((mon.personality_value & 0x3E000) >> 0xD) % 24]
        for i, block in enumerate(blocks):
            block_functions[block_shuffle[i]](block)

        return mon

    def build_binary(self) -> bytes:
        output = bytearray()
        output.extend(int.to_bytes(self.personality_value, 4, byteorder="big"))
        output.extend(int.to_bytes(self.flagsBase, 2, byteorder="big"))

        blocks = {
            "A": self.build_a_block(),
            "B": self.build_b_block(),
            "C": self.build_c_block(),
            "D": self.build_d_block(),
        }

        checksum = 0
        for block in blocks.values():
            for i in range(0x10):
                checksum += int.from_bytes(block[(2*i):(2*i)+2], byteorder="big")

        checksum &= 0xFFFF
        self.checksum = checksum

        output.extend(int.to_bytes(self.checksum, 2, byteorder="big"))

        block_shuffle = BLOCK_ORDERS[((self.personality_value & 0x3E000) >> 0xD) % 24]
        for block in block_shuffle:
            output.extend(blocks[block])

        return bytes(output)

    def __repr__(self):
        return f"{self.nickname}: Species {self.species}"
