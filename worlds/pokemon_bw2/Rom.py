from worlds.Files import APProcedurePatch, APPatchExtension
import typing
import settings
import Utils
import hashlib
import os
import bsdiff4
from .apnds.rom import Rom
from zipfile import ZipFile
from pathlib import Path

if typing.TYPE_CHECKING:
    from . import PokemonBW2World

IRDO = "0afc7974c393265d8cf23379be232a1c"
IREO = "4c65a32989c78b8070751765592b0ea6"

BW2_COMMON_PROCEDURE = [
    ("apply_patch", [])
]


class PokemonBlack2ProcedurePatch(APProcedurePatch):
    game = "Pokemon Black and White 2"
    patch_file_ending = ".apblack2"
    result_file_ending = ".nds"
    hash = IREO
    procedure = BW2_COMMON_PROCEDURE

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes(True)


class PokemonWhite2ProcedurePatch(APProcedurePatch):
    game = "Pokemon Black and White 2"
    patch_file_ending = ".apwhite2"
    result_file_ending = ".nds"
    hash = IRDO
    procedure = BW2_COMMON_PROCEDURE

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes(False)


@staticmethod
class PokemonBW2PatchExtensions(APPatchExtension):
    game = "Pokemon Black and White 2"

    @staticmethod
    def apply_patch(patch: APProcedurePatch, rom: bytes) -> bytes:
        local_rom = Rom.from_bytes(rom)
        # now search the patch files for the basepatch
        base_patch = [file for file in patch.files if "base_patch" in file]
        user_patch = [file for file in patch.files if "user_patch" in file]
        for file in base_patch:
            _, file_name = file.split("base_patch")
            file_name.replace("\\", "/")
            if file_name.startswith("/new"):
                file_name = file_name[4:]
                local_rom.files[file_name] = patch.files[file]
            elif file_name.startswith("/diff"):
                file_name = file_name[5:].split(".")[0]
                local_rom.files[file_name] = bsdiff4.patch(local_rom.files[file_name], patch.files[file])
        for file in user_patch:
            pass # these will be more complex
        return local_rom.to_bytes(False)


def patch_rom(world: "PokemonBW2World", patch: PokemonBlack2ProcedurePatch | PokemonWhite2ProcedurePatch):
    # first we should write the basepatch
    # we have to do a little bit of cursed handling here
    # because we want to write out an entire directory
    base_dir = "white_base_patch" if isinstance(patch, PokemonWhite2ProcedurePatch) else "black_base_patch"
    if world.zip_path:
        # we're in an apworld, we should load the apworld as a zip
        z = ZipFile(world.zip_path)
        for file in z.infolist():
            if not file.is_dir():
                if base_dir in file.filename:
                    _, file_dir = file.filename.split(base_dir)
                    file_dir = file_dir.replace("\\", "/")
                    patch.write_file(f"base_patch/{file_dir}", z.read(file.filename))
    else:
        # we can just walk the directory
        for path in Path(os.path.join(os.path.dirname(__file__), base_dir)).rglob("*"):
            if os.path.isfile(path):
                _, file_dir = str(path).split(base_dir)
                file_dir = file_dir.replace("\\", "/")
                if file_dir.startswith("/"):
                    file_dir = file_dir[1:]
                patch.write_file(f"base_patch/{file_dir}", open(path, "rb").read())



def get_base_rom_bytes(black: bool) -> bytes:
    rom_file: str = get_base_rom_path(black=black)
    base_rom_bytes: typing.Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(open(rom_file, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {IRDO, IREO}:
            raise Exception("Supplied Base Rom does not match known MD5 for Black 2 or White 2 US/EU/AUS release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "", black: bool = False) -> str:
    from . import PokemonBW2World
    if not file_name:
        if black:
            file_name = PokemonBW2World.settings.black_2_rom_file
        else:
            file_name = PokemonBW2World.settings.white_2_rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
