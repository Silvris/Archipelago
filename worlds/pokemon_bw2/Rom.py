from worlds.Files import APDeltaPatch
import typing
import settings
import Utils
import hashlib
import os

if typing.TYPE_CHECKING:
    from . import PokemonBW2World

class RomData:
    def __init__(self, file: str, name: typing.Optional[str] = None):
        self.file = bytearray()
        self.read_from_file(file)
        self.name = name

    def read_byte(self, offset: int):
        return self.file[offset]

    def read_bytes(self, offset: int, length: int):
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int):
        self.file[offset] = value

    def write_bytes(self, offset: int, values: typing.Sequence) -> None:
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)

    def read_from_file(self, file: str):
        with open(file, 'rb') as stream:
            self.file = bytearray(stream.read())


class PokemonBlack2DeltaPatch(APDeltaPatch):
    game = "Pokemon Black 2"
    patch_file_ending = ".apblack2"


class PokemonWhite2DeltaPatch(APDeltaPatch):
    game = "Pokemon White 2"
    patch_file_ending = ".apwhite2"


def patch_rom(world: "PokemonBW2World", player: int, rom: RomData):
    pass


def get_base_rom_bytes() -> bytes:
    rom_file: str = get_base_rom_path()
    base_rom_bytes: typing.Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(Utils.read_snes_rom(open(rom_file, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        #if basemd5.hexdigest() not in {}:
            #raise Exception("Supplied Base Rom does not match known MD5 for US or JP release. "
                            #"Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["pokemon_bw2_options"]["white_2_rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
