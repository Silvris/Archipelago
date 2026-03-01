import os
import bsdiff4

from apnds.rom import Rom

def run_diffs(base: str, new: str):
    # base is base NDS rom
    # new is the basepatch rom
    # we take a diff of individual files
    base_rom = Rom.from_bytes(open(base, 'rb').read())
    new_rom = Rom.from_bytes(open(new, 'rb').read())
    for name, file in new_rom.files.items():
        dirpath, base_name = os.path.split(name)
        if name not in base_rom.files:
            # this is a new file, output to new files directory
            new_dir = os.path.join(os.path.dirname(__file__), "base_patch", "new", dirpath[1:])
            os.makedirs(new_dir, exist_ok=True)
            open(os.path.join(new_dir, base_name), "wb").write(new_rom.files[name])
        elif file != base_rom.files[name]:
            # edited file, we need to update
            new_dir = os.path.join(os.path.dirname(__file__), "base_patch", "diff", dirpath[1:])
            os.makedirs(new_dir, exist_ok=True)
            open(os.path.join(new_dir, base_name) + ".bsdiff", "wb").write(bsdiff4.diff(base_rom.files[name], new_rom.files[name]))


def rom_test(base, new):
    with open(base, "rb") as f:
        rom = Rom.from_bytes(f.read())
    with open(new, "wb") as f:
        f.write(rom.to_bytes())

if __name__ == "__main__":
    base = input("Enter path to unpatched rom: ")
    new = input("Enter path to patched rom: ")
    #rom_test(base, r"J:\Roms\Pokemon Black 2 Romhacking\RomTest.nds")
    run_diffs(base, new)