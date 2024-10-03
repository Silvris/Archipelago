import logging
import struct
import time
import typing
import uuid

import NetUtils
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
SRAM_1_START = 0xE00000

KSS_GOURMET_RACE_WON = SRAM_1_START + 0x171D
KSS_DYNA_COMPLETED = SRAM_1_START + 0x1A63
KSS_DYNA_SWITCHES = SRAM_1_START + 0x1A64
KSS_DYNA_IRON_MAM = SRAM_1_START + 0x1A67
KSS_REVENGE_CHAPTERS = SRAM_1_START + 0x1A69
KSS_COMPLETED_SUBGAMES = SRAM_1_START + 0x1A93
KSS_ARENA_HIGH_SCORE = SRAM_1_START + 0x1AA1
KSS_BOSS_DEFEATED = SRAM_1_START + 0x1AE7  # 4 bytes
KSS_TGCO_TREASURE = SRAM_1_START + 0x1B05  # 8 bytes
KSS_TGC0_GOLD = SRAM_1_START + 0x1B0F  # 3-byte 24-bit int
KSS_COPY_ABILITIES = SRAM_1_START + 0x1B1D  # originally Milky Way Wishes deluxe essences
# Remapped for sending
KSS_SENT_DYNA_SWITCH = SRAM_1_START + 0x7A64
KSS_SENT_TGCO_TREASURE = SRAM_1_START + 0x7B05  # 8 bytes
KSS_SENT_DELUXE_ESSENCE = SRAM_1_START + 0x7B1D  # 3 bytes
# AP-received extras
KSS_RECEIVED_SUBGAMES = SRAM_1_START + 0x8000
KSS_RECEIVED_ITEMS = SRAM_1_START + 0x8002
KSS_RECEIVED_PLANETS = SRAM_1_START + 0x8004

KSS_ROMNAME = SRAM_1_START + 0x8100

class KSSSNIClient(SNIClient):
    game = "Kirby Super Star"
    patch_suffix = ".apkss"
    item_queue: typing.List[NetworkItem] = []

    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_read, snes_flush_writes
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, KSS_ROMNAME, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15) or rom_name[:3] != b"KSS":
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b111  # full remote
        ctx.allow_collect = True

        death_link = [False]  # await snes_read(ctx, KSS_DEATH_LINK_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
        return True
