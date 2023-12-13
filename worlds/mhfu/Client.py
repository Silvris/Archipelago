from __future__ import annotations

import typing

import Utils
import logging
from CommonClient import CommonContext, ClientCommandProcessor, gui_enabled, get_base_parser, server_loop
import asyncio
from websockets import client
import base64
import json
import struct

from .Quests import quest_data, base_id


ppsspp_logger = logging.getLogger("PPSSPP")
PPSSPP_REPORTING = "https://report.ppsspp.org/match/list"
PPSSPP_DEBUG = "debugger.ppsspp.org"
MHFU_SERIAL = "ULUS10391"
MHP2G_SERIAL = "ULJM05500"
FUC_SERIAL = "unknown"
PPSSPP_HELLO = {
    "event": "version",
    "name": "Archipelago: MHFU",
    "version": Utils.__version__
}
PPSSPP_STATUS = {"event": "game.status"}

MHFU_POINTERS = {
    "US": {
        "GH_VISIBLE": 0x089B1B4C,
        "VL_VISIBLE": 0x089B1D5C,
        "QUEST_COMPLETE": 0x0999E1C8
    },
    "JP": {
        "GH_VISIBLE": 0x089AEAF0,
        "VL_VISIBLE": 0x089AED00,
        "QUEST_COMPLETE": 0x09999DC8
    }
}


async def send_and_receive(ctx: MHFUContext, message: str, event: str):
    # since we can't register for a specific change in value,
    # we can just wait until we receive the one we're looking for
    await ctx.debugger.send(message)
    try:
        new_message = await asyncio.wait_for(ctx.debugger.recv(), 1)
    except asyncio.exceptions.TimeoutError:
        new_message = None
    results = []
    while new_message:
        results.append(json.loads(new_message))
        try:
            new_message = await asyncio.wait_for(ctx.debugger.recv(), 1)
        except asyncio.exceptions.TimeoutError:
            new_message = None

    return next(message for message in results if message["event"] == event)


async def connect_psp(ctx: MHFUContext, target: typing.Optional[int] = None):
    from urllib.request import urlopen, Request
    if ctx.debugger:
        del ctx.debugger
        ctx.debugger = None
    with urlopen(Request(PPSSPP_REPORTING, headers={"User-Agent": "Archipelago"})) as http:
        psps = json.loads(http.read())
    if len(psps) > 1:
        if not target:
            ppsspp_logger.error("Multiple PPSSPP instances found. Please specify the PPSSPP instance to connect to:\n"
                                  + f"Instance {psp['t']}\n" for psp in psps)
            return
        else:
            psp = psps[target]
    else:
        if psps:
            psp = psps[0]
        else:
            ppsspp_logger.error("No PPSSPP instances found to connect to. Make sure PPSSPP is running and "
                                  "\"Allow remote debugging\" is enabled in the settings.")
            return
    ctx.debugger = await client.connect(f"ws://{psp['ip']}:{psp['p']}/debugger", subprotocols=[PPSSPP_DEBUG])

    hello = await send_and_receive(ctx, json.dumps(PPSSPP_HELLO), "version")
    game_status = await send_and_receive(ctx, json.dumps(PPSSPP_STATUS), "game.status")
    if not game_status["game"] or game_status["game"]["id"] not in (MHFU_SERIAL, MHP2G_SERIAL):
        ppsspp_logger.error("Connected to PPSSPP but MHFU is not currently being played. Please run /psp when MHFU is"
                            " loaded.")
        del ctx.debugger
        ctx.debugger = None
        return
    if game_status["game"]["id"] == MHFU_SERIAL:
        ctx.lang = "US"
    else:
        ctx.lang = "JP"
    ppsspp_logger.info(f"Connected to PPSSPP {hello['version']} playing Monster Hunter Freedom Unite!")
    return


class MHFUClientCommandProcessor(ClientCommandProcessor):
    ctx: MHFUContext

    def _cmd_psp(self):
        asyncio.create_task(connect_psp(self.ctx))


class MHFUContext(CommonContext):
    game = "Monster Hunter Freedom Unite"
    tags = {"AP"}
    items_handling = 0b111
    command_processor = MHFUClientCommandProcessor
    lang: str = "JP"
    debugger: typing.Optional[client.WebSocketClientProtocol] = None
    watcher_task = None

    async def ppsspp_read_bytes(self, offset, length):
        result = await send_and_receive(self, json.dumps({
            "event": "memory.read",
            "address": offset,
            "size": length
        }), "memory.read")
        return result

    async def ppsspp_read_unsigned(self, offset, length = 8):
        if length not in (8, 16, 32):
            raise Exception("Can only read 8/16/32-bit integers.")
        result = await send_and_receive(self, json.dumps({
            "event": f"memory.read_u{length}",
            "address": offset
        }), f"memory.read_u{length}")
        return result

    async def ppsspp_write_bytes(self, offset, data):
        result = await send_and_receive(self, json.dumps({
            "event": "memory.write",
            "address": offset,
            "base64": base64.b64encode(data)
        }), "memory.write")
        return result

    async def ppsspp_write_unsigned(self, offset, value, length = 8):
        if length not in (8, 16, 32):
            raise Exception("Can only read 8/16/32-bit integers.")
        if value > pow(2, length):
            raise Exception("Attempted a write greater than the possible size of the location.")
        result = await send_and_receive(self, json.dumps({
            "event": f"memory.write_u{length}",
            "address": offset,
            "value": value
        }), f"memory.write_u{length}")
        return result

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(MHFUContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class MHFUManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("PPSSPP", "PPSSPP"),
            ]
            base_title = "Archipelago Monster Hunter Freedom Unite Client"

        self.ui = MHFUManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx):
    while not ctx.exit_event.is_set():
        try:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()
            if ctx.server is None or ctx.slot is None:
                continue

            new_checks = []
            gh_visible = await ctx.ppsspp_read_bytes(MHFU_POINTERS[ctx.lang]["GH_VISIBLE"], 0x210)
            completion_bytes = await ctx.ppsspp_read_bytes(MHFU_POINTERS[ctx.lang]["QUEST_COMPLETE"], 63)
            quest_completion = base64.b64decode(completion_bytes["base64"])
            for id, quest in enumerate(quest_data):
                flag = int(quest["flag"])
                mask = int(quest["mask"])
                if flag >= 0 and mask >= 0:
                    if quest_completion[flag] & (1 << mask) and base_id + id not in ctx.checked_locations:
                        new_checks.append(id + base_id)

            if new_checks:
                for new_check_id in new_checks:
                    ctx.locations_checked.add(new_check_id)
                    location = ctx.location_names[new_check_id]
                    ppsspp_logger.info(
                        f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
        except Exception as ex:
            Utils.messagebox("Error", str(ex), True)


async def main(args):

    ctx = MHFUContext(args.connect, args.password)
    """
    chat_socket = MySocket()
    chat_socket.connect(socket.gethostbyname(socket.getfqdn()), 27312)
    packet = bytes((
        *bytes([1]),
        *struct.pack(
            "IH",
            getnode() & 0xFFFFFFFF,
            getnode() >> 32
        ),
        *bytearray("Archipelago", 'utf-8') + bytes([0] * (128 - 11)),
        *bytearray("ULUS10391", 'utf-8')
        )
    )
    asyncio.create_task(keep_alive_and_parse(ctx))
    chat_socket.send(packet)
    chat_socket.send(bytes((*bytes([2]), *bytes("MHP2Q000", 'utf-8'))))
    ctx.chat_socket = chat_socket
    """
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    print("Connecting")
    await connect_psp(ctx)
    ctx.watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")
    await ctx.exit_event.wait()
    if ctx.debugger and not ctx.debugger.closed:
        await ctx.debugger.close()
    await ctx.shutdown()



def launch():
    import colorama
    colorama.init()
    args = get_base_parser().parse_args()
    asyncio.run(main(args))
    colorama.deinit()