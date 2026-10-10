from __future__ import annotations

import argparse
import asyncio
import logging
from typing import TYPE_CHECKING

import dolphin_memory_engine
import Utils
from CommonClient import CommonContext, ClientCommandProcessor, gui_enabled, get_base_parser, server_loop

if TYPE_CHECKING:
    import kvui

BATTLE_REV_SAVE_FILE_PTR = 0x8045DE80
BATTLE_REV_CURRENT_MODE_PTR = 0x804569C0
BATTLE_REV_SAVE_FILE_INDEX = 0x50
BATTLE_REV_SAVE_START = 0x380
BATTLE_REV_SAVE_SIZE = 0x6FF00  # mult by current save index to find current player
BATTLE_REV_PARTY_OFS = 0xCC
BATTLE_REV_BOX_OFS = 0x5F8
BATTLE_REV_PKM_SIZE = 0x88
BATTLE_REV_PARTY_PKM_SIZE = BATTLE_REV_PKM_SIZE + 0x54
BATTLE_REV_BOX_SIZE = BATTLE_REV_PKM_SIZE * 30
BATTLE_REV_ASSOC_TID = 0x124E0  # First byte is here, second byte is +7
BATTLE_REV_COUPONS = 0x124E1  # 3-byte
BATTLE_REV_ASSOC_SID = 0x124E5  # short


logger = logging.getLogger("Wii")


class PBRCommandProcessor(ClientCommandProcessor):
    ctx: PBRContext

    def _cmd_debug_display(self):
        self.ctx.display_hooked = True


class PBRContext(CommonContext):
    game = "Pokemon Battle Revolution"
    tags = {"AP"}
    items_handling = 0b111
    display_hooked = False
    command_processor = PBRCommandProcessor

    def make_gui(self) -> "type[kvui.GameManager]":
        from kvui import GameManager

        class PBRManager(GameManager):
            base_title = "Archipelago Pokémon Battle Revolution Client"
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Wii", "Wii")
            ]
        return PBRManager

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def debug_display(self):
        from .gen4_pokemon_structure import Gen4Pokemon
        logger.warning(f"Hooked.")
        save_base = dolphin_memory_engine.read_word(BATTLE_REV_SAVE_FILE_PTR)
        save_slot = dolphin_memory_engine.read_byte(save_base + BATTLE_REV_SAVE_FILE_INDEX)
        save_ptr = save_base + (save_slot * BATTLE_REV_SAVE_SIZE) + BATTLE_REV_SAVE_START
        tid_low = dolphin_memory_engine.read_byte(save_ptr + BATTLE_REV_ASSOC_TID)
        tid_high = dolphin_memory_engine.read_byte(save_ptr + BATTLE_REV_ASSOC_TID + 7)
        tid = tid_high << 8 | tid_low
        sid = int.from_bytes(dolphin_memory_engine.read_bytes(save_ptr + BATTLE_REV_ASSOC_SID, 2), byteorder="big")
        coupons = int.from_bytes(dolphin_memory_engine.read_bytes(save_ptr + BATTLE_REV_COUPONS, 3), byteorder="big")
        logger.warning(f"TID: {tid}, SID: {sid}, Coupons: {coupons}")
        for pkm in range(6):
            species = int.from_bytes(dolphin_memory_engine.read_bytes(save_ptr + BATTLE_REV_PARTY_OFS +
                                                                      (pkm * BATTLE_REV_PARTY_PKM_SIZE) + 8, 2),
                                     byteorder="big")
            if species != 0:
                logger.warning(f"Party: species: {species}, pkm: {pkm}")
        for box in range(18):
            for pkm in range(30):
                mon_bytes = dolphin_memory_engine.read_bytes(save_ptr +
                                                                    (box * BATTLE_REV_BOX_SIZE) +
                                                                     BATTLE_REV_BOX_OFS +
                                                                     (pkm * BATTLE_REV_PKM_SIZE), 0x88)
                mon = Gen4Pokemon.create_from_binary(mon_bytes)
                test_mon = Gen4Pokemon.create_from_binary(mon.build_binary())
                if mon.species != 0:
                    logger.warning(f"species: {mon.species}, pkm: {pkm}, box: {box}, valid: {mon.build_binary() == mon_bytes}")


async def game_watcher(ctx: PBRContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()
            if not dolphin_memory_engine.is_hooked():
                dolphin_memory_engine.hook()
                continue
            if not ctx.slot:
                continue
            if ctx.display_hooked:
                await ctx.debug_display()
                ctx.display_hooked = False
        except Exception as ex:
            import traceback
            Utils.messagebox("Error", str(ex), True)
            logger.error(traceback.format_exc())






async def main(args: "argparse.Namespace") -> None:
    ctx = PBRContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    ctx.watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch_pbr_client(*launch_args: str) -> None:
    import colorama
    import urllib.parse
    colorama.init()
    parser = get_base_parser()
    parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(launch_args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            if url.password:
                args.password = urllib.parse.unquote(url.password)
            if url.username:
                args.connect = f'{urllib.parse.unquote(url.username)}:None@{url.hostname}:{url.port}'
            else:
                args.connect = f'{url.hostname}:{url.port}'

        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    asyncio.run(main(args))
    colorama.deinit()