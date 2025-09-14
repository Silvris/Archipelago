from __future__ import annotations

import random
import traceback

from operator import itemgetter
import Utils
import logging
from CommonClient import CommonContext, ClientCommandProcessor, gui_enabled, get_base_parser, server_loop
import asyncio
from websockets import client, Subprotocol
import base64
import json
import struct
from zlib import crc32
from typing import Tuple, Any, TYPE_CHECKING
from enum import IntEnum
from time import time

from NetUtils import NetworkItem, ClientStatus
from .data.trap_link import trap_link_matches, local_trap_to_type
from .quests import (quest_data, base_id, goal_quests, get_quest_by_id,
                     get_proper_name, location_name_to_id, SlotQuestInfo)
from .items import item_name_to_id, item_id_to_name, item_name_groups
from .data.monsters import elder_dragons, monster_lookup
from .data.equipment import blademaster, gunner, blademaster_upgrades, gunner_upgrades, \
    helms, chests, arms, waists, legs
from .data.item_gifts import item_gifts, decoration_gifts

if TYPE_CHECKING:
    import argparse

class DeathState(IntEnum):
    alive = 0
    killing_player = 1
    dead = 2

ppsspp_logger = logging.getLogger("PPSSPP")
logger = logging.getLogger("Client")
PPSSPP_REPORTING = "https://report.ppsspp.org/match/list"
PPSSPP_DEBUG = "debugger.ppsspp.org"
MHFU_SERIAL = "ULUS10391"
MHFU_EU_SERIAL = "ULES01213"
MHP2G_SERIAL = "ULJM05500"
SERIAL_TO_LANG = {
    MHFU_SERIAL: "US",
    MHFU_EU_SERIAL: "EU",
    MHP2G_SERIAL: "JP",
}
PPSSPP_HELLO = {
    "event": "version",
    "name": "Archipelago: MHFU",
    "version": Utils.__version__,
    "ticket": "AP_HELLO"
}
PPSSPP_STATUS = {"event": "game.status", "ticket": "AP_STATUS"}
PPSSPP_CONFIG = {"event": "broadcast.config.set", "ticket": "AP_CONFIG", "disallowed": {"input": True}}

MHFU_POINTERS = {
    "US": {
        "GH_VISIBLE": 0x089B1B4C,
        "VL_VISIBLE": 0x089B1D5C,
        "QUEST_COMPLETE": 0x0999E1C8,
        "GH_KEYS": 0x089B1EA0,
        "VL_KEYS": 0x089B1F10,
        "EQUIP_CHEST": 0x0999A2E8,
        "ITEM_CHEST": 0x0999D1C8,
        "SHOP_HEAD": 0x0893B938,
        "SHOP_CHEST": 0x0893E59A,
        "SHOP_ARM": 0x089411C8,
        "SHOP_WAIST": 0x08943D0C,
        "SHOP_LEG": 0x0894681C,
        "SHOP_GREAT_LONG": 0x0894944C,
        "SHOP_LANCE_GUN": 0x0894A19A,
        "SHOP_SNS_DUAL": 0x0894AD7C,
        "SHOP_HAMMER_HORN": 0x0894BACA,
        "SHOP_GUNNER": 0x0894C832,
        "BLADEMASTER_UPGRADES": 0x0894FAE4,
        "GUNNER_UPGRADES": 0x089578AC,
        "NARGA_HYPNOC_CUTSCENE": 0x0999A2D4,
        "TREASURE_SCORE": 0x09A015A0,
        "ZENNY": 0x09A03490,
        "CURRENT_OVL": 0x09A5F320,
        "RESET_ACTION": 0x090B3755,
        "SET_ACTION": 0x090B3818,
        "POISON_TIMER": 0x090B3908,
        "QUEST_TIMER": 0x09A05F10,
        "QUEST_REWARD": 0x09A05F14,
        "QUEST_UNKN": 0x09A05F18,
        "QUEST_STATUS": 0x09A05F1C,
        "AP_SAVE": 0x099FE590
    },
    "EU": {
        "GH_VISIBLE": 0x089B1A2C,
        "VL_VISIBLE": 0x089B1C3C,
        "QUEST_COMPLETE": 0x0999E088,
        "GH_KEYS": 0x089B1D80,
        "VL_KEYS": 0x089B1DF0,
        "EQUIP_CHEST": 0x0999A1A8,
        "ITEM_CHEST": 0x0999D088,
        "SHOP_HEAD": 0x0893B818,
        "SHOP_CHEST": 0x0893E47A,
        "SHOP_ARM": 0x089410A8,
        "SHOP_WAIST": 0x08943BEC,
        "SHOP_LEG": 0x089466FC,
        "SHOP_GREAT_LONG": 0x0894932C,
        "SHOP_LANCE_GUN": 0x0894A07A,
        "SHOP_SNS_DUAL": 0x0894AC5C,
        "SHOP_HAMMER_HORN": 0x0894B9AA,
        "SHOP_GUNNER": 0x0894C712,
        "BLADEMASTER_UPGRADES": 0x0894F9C4,
        "GUNNER_UPGRADES": 0x0895778C,
        "NARGA_HYPNOC_CUTSCENE": 0x0999A194,
        "TREASURE_SCORE": 0x09A01460,
        "ZENNY": 0x09A03350,
        "CURRENT_OVL": 0x09A5F220,
        "RESET_ACTION": 0x090B3615,
        "SET_ACTION": 0x090B36D8,
        "POISON_TIMER": 0x090B37C8,
        "QUEST_TIME": 0x09A05DD0,
        "QUEST_REWARD": 0x09A05DD4,
        "QUEST_UNKN": 0x09A05DD8,
        "QUEST_STATUS": 0x09A05DDC,
        "AP_SAVE": 0x099FE450,
    },
    "JP": {
        "GH_VISIBLE": 0x089AEAF0,
        "VL_VISIBLE": 0x089AED00,
        "QUEST_COMPLETE": 0x09999DC8,
        "GH_KEYS": 0x089AEE44,
        "VL_KEYS": 0x089AEEB4,
        "EQUIP_CHEST": 0x9995EE8,
        "ITEM_CHEST": 0x09998DC8,
        "SHOP_HEAD": 0x08938D14,
        "SHOP_CHEST": 0x0893B976,
        "SHOP_ARM": 0x0893E5A4,
        "SHOP_WAIST": 0x089410E8,
        "SHOP_LEG": 0x08943BF8,
        "SHOP_GREAT_LONG": 0x08946828,
        "SHOP_LANCE_GUN": 0x08947576,
        "SHOP_SNS_DUAL": 0x08948158,
        "SHOP_HAMMER_HORN": 0x08948EA6,
        "SHOP_GUNNER": 0x08949C0E,
        "BLADEMASTER_UPGRADES": 0x0894CEC0,
        "GUNNER_UPGRADES": 0x08954C88,
        "NARGA_HYPNOC_CUTSCENE": 0x09995ED4,
        "TREASURE_SCORE": 0x099FD1A0,
        "ZENNY": 0x099FF090,
        "CURRENT_OVL": 0x09A5A5A0,
        "RESET_ACTION": 0x090AF355,  # byte
        "SET_ACTION": 0x090AF418,  # half
        "POISON_TIMER": 0x090AF508,  # half
        "QUEST_TIMER": 0x09A01B10,  # half
        "QUEST_REWARD": 0x09A01B14,  # half
        "QUEST_UNKN": 0x09A01B18,  # half
        "QUEST_STATUS": 0x09A01B1C,  # half
        "AP_SAVE": 0x099FC080,  # 96th GC slot, hopefully you don't have 96 lol
        # "QUEST_VISUAL_GOAL": 0x09B1DA48,
        # "QUEST_VISUAL_MON": 0x9B1DDAE8,
    }
}

MHFU_BREAKPOINTS = {
    # logFormat: memory, address, size, enabled, log, read, write, change
    # enabled being "do we want to pause emulation here"
    # disabled effectively acting as an event system
    # memory being this is a memory breakpoint, else it's CPU
    # CPU breakpoints don't use read/write/change
    "US": {
        "QUEST_LOAD": (True, 0x08A5C560, 1, True, True, True, False, False),
        "MONSTER_LOAD": (False, 0x08871C2C, 1, True, True, False, False, False),
        "QUEST_VISUAL_LOAD": (False, 0x09A8826C, 1, False, True, False, False, False),
        "QUEST_VISUAL_TYPE": (False, 0x09A87F9C, 1, True, True, False, False, False)
    },
    "EU": {
        "QUEST_LOAD": (True, 0x08A5C440, 1, True, True, True, False, False),
        "MONSTER_LOAD": (False, 0x08871C2C, 1, True, True, False, False, False),
        "QUEST_VISUAL_LOAD": (False, 0x09A8816C, 1, False, True, False, False, False),
        "QUEST_VISUAL_TYPE": (False, 0x09A87E9C, 1, True, True, False, False, False)
    },
    "JP": {
        "QUEST_LOAD": (True, 0x08A57510, 1, True, True, True, False, False),
        "MONSTER_LOAD": (False, 0x08871C24, 1, True, True, False, False, False),
        "QUEST_VISUAL_LOAD": (False, 0x09A8346C, 1, False, True, False, False, False),
        "QUEST_VISUAL_TYPE": (False, 0x09A8319C, 1, True, True, False, False, False)
    },

}

MHFU_BREAKPOINT_ARGS = {
    # do this so we can just pass the former directly, while parse this one
    # this lets us pull register info from the breakpoint
    "MONSTER_LOAD": ["{v0+0x2E4:p}"],
    "QUEST_VISUAL_TYPE": ["{v0},{v0+0x18:p}"],
    "QUEST_VISUAL_LOAD": ["{v0-0x448},{v0-0xa8},{s4+0x20:p}"]
}

ACTIONS = {
    -1: 0x0300,  # Kill Player
    10: 0x0072,  # Farcaster
    11: 0x0215,  # Sleep
    13: 0x0216,  # Paralysis
    14: 0x021B,  # Snowman
    15: 0x0019,  # Use Item
    16: 0x0202,  # Knockback
    17: 0x0204,  # Blowback
    18: 0x0219,  # Roar
    19: 0x0205,  # Trip
}

KEY_OFFSETS = {
    # hub, rank, star: offset size
    (0, 1, 0): 0,
    (0, 1, 1): 12,
    (0, 1, 2): 24,
    (0, 2, 0): 36,
    (0, 2, 1): 48,
    (0, 2, 2): 60,
    (0, 3, 0): 72,
    (0, 3, 1): 84,
    (0, 3, 2): 96,
    (1, 0, 0): 0,
    (1, 0, 1): 8,
    (1, 0, 2): 20,
    (1, 0, 3): 34,
    (1, 0, 4): 46,
    (1, 0, 5): 56,
    (1, 1, 0): 64,
    (1, 1, 1): 78,
    (1, 1, 2): 90
}

WEAPON_GROUPS = {
    0: [0, 7],
    1: [2, 8],
    2: [4, 6],
    3: [3, 9],
    4: [1, 5, 10],
    5: [i for i in range(11)]
}

TREASURE_SCORES = {
    "m04001": (20000, 30000),
    "m04002": (30000, 35000),
    "m04003": (30000, 35000),
    "m04004": (30000, 40000),
    "m04005": (30000, 40000),
    "m04006": (40000, 45000),
    "m04007": (40000, 50000),
}


def split_log_mem(data: str) -> tuple[int, int]:
    # PPSSPP uses the format %x[%x] for memory logging
    # logging both pointer and memory
    pointer, data = data.split("[")
    return int(pointer, 16), int(data[:-1], 16)


async def handle_logs(ctx: MHFUContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()
            if not ctx.debugger or ctx.debugger.closed:
                continue
            if ctx.server is None or ctx.slot is None:
                continue
            if ctx.breakpoint_queue:
                log = ctx.breakpoint_queue.pop(0)
                if log["channel"] in ("MEMMAP", "JIT"):
                    # we hit a breakpoint
                    bp = log["message"].replace("\n", "").rsplit(" ")[-1]
                    print(bp)
                    if bp == "QUEST_LOAD":
                        if ctx.randomize_quest:
                            quest_base = MHFU_BREAKPOINTS[ctx.lang][bp][1]
                            quest_id = (await ctx.ppsspp_read_unsigned(quest_base + 100, "LOAD_QUEST_ID", 16))["value"]
                            large_mon_ptr_ptr = quest_base + 0x14
                            large_mon_ptr = (await ctx.ppsspp_read_unsigned(large_mon_ptr_ptr,
                                                                            "LARGE_MON_PTR", 32))["value"]
                            large_mon_id_ptr = await ctx.ppsspp_read_unsigned(large_mon_ptr + quest_base + 8,
                                                                              "LARGE_MON_ID", 32)
                            large_mon_info_ptr = await ctx.ppsspp_read_unsigned(large_mon_ptr + 12 + quest_base,
                                                                                "LARGE_MON_INFO", 32)
                            large_mons = struct.unpack("IIII",
                                                       base64.b64decode((await ctx.ppsspp_read_bytes(
                                                           large_mon_id_ptr["value"] + quest_base, 16, "LARGE_MONS"))[
                                                                            "base64"]))
                            mons = {}
                            for idx, mon in enumerate([mon for mon in large_mons if mon != 0xFFFFFFFF]):
                                # pull the mons
                                mons[idx] = await ctx.ppsspp_read_bytes(large_mon_info_ptr["value"] +
                                                                        quest_base + (idx * 60),
                                                                        60, "LARGE_MONSTER")
                            # print(mons)
                            # apply difficulty modifier
                            if mons and ctx.quest_randomization:
                                quest_str = str("%.5i" % quest_id)
                                info_out = bytearray()
                                quest_mons = ctx.quest_info[quest_str]["monsters"]
                                for mon in mons:
                                    mon_data = bytearray(base64.b64decode(mons[mon]["base64"]))
                                    if ctx.quest_randomization:
                                        mon_data[0:4] = struct.pack("I", quest_mons[mon])
                                    info_out.extend(mon_data)
                                await ctx.ppsspp_write_bytes(large_mon_info_ptr["value"] + quest_base,
                                                             info_out, "WRITE_LARGE_MON_INFO")
                                # need to write new monster ids
                                await ctx.ppsspp_write_bytes(large_mon_id_ptr["value"] + quest_base,
                                                             struct.pack("IIII", *quest_mons,
                                                                         *[0xFFFFFFFF] * (4 - len(quest_mons))),
                                                             "WRITE_LARGE_MON_ID")
                                # now pick one to be the quest target
                                await ctx.ppsspp_write_bytes(quest_base + 0x4C, struct.pack("I", 1), "QTYPE")
                                target_mons = ctx.quest_info[quest_str]["targets"].copy()
                                first = target_mons.pop()
                                await ctx.ppsspp_write_bytes(quest_base + 0x6C, struct.pack("I", 1), "MON1_GOAL")
                                await ctx.ppsspp_write_bytes(quest_base + 0x70, struct.pack("HH", first, 1), "MON1")
                                if target_mons:
                                    # secondary goal
                                    target_mon = target_mons.pop()
                                    await ctx.ppsspp_write_bytes(quest_base + 0x74, struct.pack("I", 1), "MON2_GOAL")

                                    await ctx.ppsspp_write_bytes(quest_base + 0x78,
                                                                 struct.pack("HH", target_mon, 1), "MON2")
                                else:
                                    # need to null these 3
                                    await ctx.ppsspp_write_bytes(quest_base + 0x74,
                                                                 struct.pack("IHH", 0, 0, 0), "MON2_NULL")
                        # this gets pinged twice during quest load, we edit the first and fall through the second
                        ctx.randomize_quest = not ctx.randomize_quest
                    elif "MONSTER_LOAD" in bp:
                        bp, mon_addr = bp.split("|")
                        mon_address, health = split_log_mem(mon_addr)
                        health = min(max(int(health * ctx.quest_multiplier), 1), 0xFFFF)
                        await ctx.ppsspp_write_unsigned(mon_address, health, "HEALTH1", 16)
                        await ctx.ppsspp_write_unsigned(mon_address + 0x13A, health, "HEALTH2", 16)

                    elif "QUEST_VISUAL_LOAD" in bp:
                        bp, args = bp.split("|")
                        goal, mons, qid = args.split(",")
                        _, quest = split_log_mem(qid)
                        quest_id = quest & 0xFFFF
                        quest_info = ctx.quest_info[f"{quest_id:05}"]
                        if "targets" in quest_info and quest_info["targets"]:
                            # now we can construct the strings
                            targets = [mon for mon in quest_info["targets"]]
                            targets.reverse()
                            target = targets.pop()
                            is_slay = target in elder_dragons.values()
                            goal_str = f"{'Slay' if is_slay else 'Hunt'} " \
                                       f"{'the' if is_slay else ('an' if monster_lookup[target].lower()[0] in ('a', 'e', 'i', 'o', 'u') else 'a')}" \
                                       f" {monster_lookup[target]} "
                            if targets:
                                target = targets.pop()
                                is_slay_2 = target in elder_dragons.values()
                                if is_slay != is_slay_2:
                                    goal_str += f"and \n{'Slay' if is_slay_2 else 'Hunt'} "
                                else:
                                    goal_str += "and \n"
                                goal_str += f"{'the' if is_slay_2 else ('an' if monster_lookup[target].lower()[0] in ('a', 'e', 'i', 'o', 'u') else 'a')}"
                                goal_str += f" {monster_lookup[target]}"
                            await ctx.ppsspp_write_bytes(int(goal, 16),
                                                         goal_str.encode("ascii") + b"\x00", "Q_TARGET")
                        # now monsters
                        mons_str = f"\n".join([monster_lookup[mon] for mon in quest_info["monsters"]])
                        await ctx.ppsspp_write_bytes(int(mons, 16), mons_str.encode("ascii") + b"\x00", "Q_MONSTERS")

                    elif "QUEST_VISUAL_TYPE" in bp:
                        bp, args = bp.split("|")
                        qaddr, quest_id_str = args.split(",")
                        quest_addr = int(qaddr, 16)
                        quest_id_addr, quest_mix = split_log_mem(quest_id_str)
                        quest_str = str("%.5i" % (quest_mix & 0xFFFF))
                        if "targets" in ctx.quest_info[quest_str] and ctx.quest_info[quest_str]["targets"]:
                            qtype = 0x4
                            if any(monster in elder_dragons.values() for monster in ctx.quest_info[quest_str]["targets"]):
                                qtype = 0x1
                            await ctx.ppsspp_write_bytes(quest_addr, qtype.to_bytes(1, "little"), "Q_VTYPE")

                    if MHFU_BREAKPOINTS[ctx.lang][bp][3]:
                        # this break point stops emulation, we need to restart it
                        await send_without_receive(ctx, json.dumps({"event": "cpu.resume", "ticket": "RESTART"}))
        except Exception as ex:
            Utils.messagebox("Error", str(ex), True)
            logger.error(traceback.format_exc())


async def receive_all(ctx: MHFUContext) -> None:
    import websockets
    while not ctx.exit_event.is_set():
        try:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()
            if not ctx.debugger or ctx.debugger.closed:
                continue
            try:
                new_message = await ctx.debugger.recv()
            except websockets.exceptions.ConnectionClosedError:
                continue
            event = json.loads(new_message)
            if event["event"] == "log":
                ctx.breakpoint_queue.append(event)
            elif "ticket" in event:
                ctx.outgoing_tickets[event["ticket"]] = event
        except Exception as ex:
            Utils.messagebox("Error", str(ex), True)
            logger.error(traceback.format_exc())


async def send_and_receive(ctx: MHFUContext, message: str, ticket: str) -> dict[str, Any]:
    # since we can't register for a specific change in value,
    # we can just wait until we receive the one we're looking for
    if not ticket:
        raise Exception("Cannot perform read/write without valid ticket.")
    if ctx.debugger:
        await ctx.debugger.send(message)
        while ticket not in ctx.outgoing_tickets:
            await asyncio.sleep(0.125)
        return ctx.outgoing_tickets.pop(ticket)
    return {}

async def send_without_receive(ctx: MHFUContext, message: str) -> None:
    # cpu actions do not return tickets
    if ctx.debugger:
        await ctx.debugger.send(message)


async def connect_psp(ctx: MHFUContext, target: int | None = None) -> None:
    from urllib.request import urlopen, Request
    if ctx.debugger:
        del ctx.debugger
        ctx.debugger = None
    with urlopen(Request(PPSSPP_REPORTING, headers={"User-Agent": "Archipelago"})) as http:
        psps = json.loads(http.read())
    psps = [psp for psp in psps if ":" not in psp["ip"]]
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
    ctx.debugger = await client.connect(f"ws://{psp['ip']}:{psp['p']}/debugger",
                                        subprotocols=[Subprotocol(PPSSPP_DEBUG)])

    hello = await send_and_receive(ctx, json.dumps(PPSSPP_HELLO), "AP_HELLO")
    game_status = await send_and_receive(ctx, json.dumps(PPSSPP_STATUS), "AP_STATUS")
    if not game_status["game"] or game_status["game"]["id"] not in SERIAL_TO_LANG:
        ppsspp_logger.error("Connected to PPSSPP but MHFU is not currently being played. Please run /psp when MHFU is"
                            " loaded.")
        del ctx.debugger
        ctx.debugger = None
        return
    ctx.lang = SERIAL_TO_LANG[game_status["game"]["id"]]
    ppsspp_logger.info(f"Connected to PPSSPP {hello['version']} playing Monster Hunter Freedom Unite!")
    config = await send_and_receive(ctx, json.dumps(PPSSPP_CONFIG), "AP_CONFIG")
    for bp in MHFU_BREAKPOINTS[ctx.lang]:
        if MHFU_BREAKPOINTS[ctx.lang][bp][0]:
            await send_and_receive(ctx, json.dumps(
                dict(zip(["event", "ticket", "address", "size", "enabled",
                          "log", "read", "write", "change", "logFormat"],
                         ["memory.breakpoint.add", "MEM_BREAKPOINT", *MHFU_BREAKPOINTS[ctx.lang][bp][1:],
                          '|'.join([bp, *MHFU_BREAKPOINT_ARGS.get(bp, list())])]
                         ))), "MEM_BREAKPOINT")
        else:
            await send_and_receive(ctx, json.dumps(
                dict(zip(
                    ["event", "ticket", "address", "enabled", "log", "logFormat"],
                    ["cpu.breakpoint.add", "CPU_BREAKPOINT", MHFU_BREAKPOINTS[ctx.lang][bp][1],
                     MHFU_BREAKPOINTS[ctx.lang][bp][3], MHFU_BREAKPOINTS[ctx.lang][bp][4],
                     '|'.join([bp, *MHFU_BREAKPOINT_ARGS.get(bp, list())])]
                ))
            ), "CPU_BREAKPOINT")
    return


class MHFUClientCommandProcessor(ClientCommandProcessor):
    ctx: MHFUContext

    def _cmd_psp(self) -> None:
        asyncio.create_task(connect_psp(self.ctx))


class MHFUContext(CommonContext):
    game = "Monster Hunter Freedom Unite"
    tags = {"AP"}
    items_handling = 0b111
    command_processor = MHFUClientCommandProcessor
    lang: str = "JP"
    debugger: client.WebSocketClientProtocol | None = None
    watcher_task: asyncio.Task[None] | None = None
    update_task: asyncio.Task[None] | None = None
    breakpoint_task: asyncio.Task[None] | None = None
    socket_task: asyncio.Task[None] | None = None
    want_slot_data: bool = True
    server_seed_name: str | None = None
    outgoing_tickets: dict[str, dict[str, Any]] = {}
    breakpoint_queue: list[dict[str, Any]] = []
    last_trap_link: float = -1

    # game info
    recv_index = -1
    death_link: int = 0
    goal: int = 0
    goal_quest: str = "m03233"  # This is Ukanlos, pick the furthest out to potentially avoid collision
    unlocked_keys: int = 0
    required_keys: int = 0
    refresh: bool = False
    rank_requirements: dict[Tuple[int, int, int], int] = {}
    weapon_status: dict[int, set[int]] = {
        0: set(),  # Great Sword
        1: set(),  # Heavy Bowgun
        2: set(),  # Hammer
        3: set(),  # Lance
        4: set(),  # Sword and Shield
        5: set(),  # Light Bowgun
        6: set(),  # Dual Blades
        7: set(),  # Long Sword
        8: set(),  # Hunting Horn
        9: set(),  # Gunlance
        10: set(),  # Bow
    }
    armor_status: set[int] = set()
    quest_randomization: bool = False
    quest_info: dict[str, SlotQuestInfo] = {}
    quest_multiplier: float = 1.0
    cash_only: bool = False
    item_queue: list[NetworkItem] = []
    trap_queue: list[int] = []
    set_cutscene: bool | None = None
    trap_link: bool = False
    allowed_traps: list[int] = []

    # intermittent
    randomize_quest: bool = True
    death_state: DeathState = DeathState.alive

    async def ppsspp_read_bytes(self, offset: int, length: int, ticket: str) -> dict[str, Any]:
        result = await send_and_receive(self, json.dumps({
            "event": "memory.read",
            "address": offset,
            "size": length,
            "ticket": ticket,
        }), ticket)
        return result

    async def ppsspp_read_unsigned(self, offset: int, ticket: str, length: int = 8) -> dict[str, Any]:
        if length not in (8, 16, 32):
            raise Exception("Can only read 8/16/32-bit integers.")
        result = await send_and_receive(self, json.dumps({
            "event": f"memory.read_u{length}",
            "address": offset,
            "ticket": ticket
        }), ticket)
        return result

    async def ppsspp_read_string(self, offset: int, ticket: str) -> dict[str, Any]:
        result = await send_and_receive(self, json.dumps({
            "event": "memory.readString",
            "address": offset,
            "ticket": ticket
        }), ticket)
        return result

    async def ppsspp_write_bytes(self, offset: int, data: bytes | bytearray, ticket: str) -> dict[str, Any]:
        result = await send_and_receive(self, json.dumps({
            "event": "memory.write",
            "address": offset,
            "base64": str(base64.b64encode(data), "utf-8"),
            "ticket": ticket
        }), ticket)
        return result

    async def ppsspp_write_unsigned(self, offset: int, value: int,
                                    ticket: str, length: int = 8) -> dict[str, Any]:
        if length not in (8, 16, 32):
            raise Exception("Can only write 8/16/32-bit integers.")
        if value > pow(2, length):
            raise Exception("Attempted a write greater than the possible size of the location.")
        result = await send_and_receive(self, json.dumps({
            "event": f"memory.write_u{length}",
            "address": offset,
            "value": value,
            "ticket": ticket,
        }), ticket)
        return result

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(MHFUContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def get_key_binary(self) -> None:
        target = 65535
        for hub, rank, star in sorted(self.rank_requirements, key=itemgetter(0, 1, 2)):
            if (hub, rank, star) in KEY_OFFSETS:
                print(self.rank_requirements[hub, rank, star], self.unlocked_keys)
                address = MHFU_POINTERS[self.lang]["GH_KEYS" if hub == 0 else "VL_KEYS"]
                address += KEY_OFFSETS[hub, rank, star]
                data = bytearray()
                if self.unlocked_keys >= self.rank_requirements[hub, rank, star]:
                    data.extend([0] * 10)
                else:
                    if target > self.rank_requirements[hub, rank, star]:
                        target = self.rank_requirements[hub, rank, star]
                    data.extend(struct.pack("HHHHH", 30001, 0, 0, 0, 0))
                if (hub, rank, star) != (1, 0, 0):
                    data.extend([0] * 2)
                await self.ppsspp_write_bytes(address, data, "WRITE_KEYS")
        if self.ui:
            self.ui.update_keys(self.unlocked_keys, target)

    async def set_equipment_status(self) -> None:
        equip_group: str
        length: int
        remap: dict[int, int]
        equipment_type: int
        weapon_type: int
        equip_rarity: int
        for equip_group, length, remap, equipment_type in zip([
            "SHOP_HEAD", "SHOP_CHEST", "SHOP_ARM", "SHOP_WAIST", "SHOP_LEG",
            "SHOP_GREAT_LONG", "SHOP_LANCE_GUN", "SHOP_SNS_DUAL", "SHOP_HAMMER_HORN", "SHOP_GUNNER"],
                [11362, 11310, 11076, 11024, 11284,
                 3406, 3042, 3406, 3224, 7878],
                [
                    helms, chests, arms, waists, legs, blademaster, blademaster, blademaster, blademaster, gunner],
                [
                    1, 2, 3, 4, 0, 5, 5, 5, 5, 6]
        ):
            create_data = bytearray(base64.b64decode(
                (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang][equip_group], length, "READ_CREATE"))[
                    "base64"]))
            for i in range(length // 0x1A):
                equip_type, _, equip_id = struct.unpack("BBH", create_data[0x1A * i: (0x1A * i) + 4])
                if equipment_type in (5, 6):
                    weapon_type, equip_rarity = remap[equip_id]
                    if equip_rarity + 1 not in self.weapon_status[weapon_type]:
                        create_data[0x1A * i] = 0x10  # somehow this doesn't crash the game
                    else:
                        create_data[0x1A * i] = equipment_type
                else:
                    equip_rarity = remap[equip_id]
                    if equip_rarity + 1 not in self.armor_status:
                        create_data[0x1A * i] = 0x10
                    else:
                        create_data[0x1A * i] = equipment_type
                create_data[(0x1A * i) + 1] = 0x1  # this unhides every weapon/armor, so it should always be visible
                if self.cash_only:
                    create_data[(0x1A * i) + 4: (0x1A * i) + 20] = [0] * 16
            await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang][equip_group],
                                          bytes(create_data), "WRITE_CREATE")

        bm_upgrade_data = bytearray(base64.b64decode(
            (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang]["BLADEMASTER_UPGRADES"],
                                          32200, "READ_UPGRADE_BM"))["base64"]))
        for i in range(1, 1150):
            if self.cash_only:
                bm_upgrade_data[(i * 0x1C): (i * 0x1C) + 0x10] = [0] * 16
            for j in range(6):
                if blademaster_upgrades[i][j] > 0:
                    weapon_type, equip_rarity = blademaster[blademaster_upgrades[i][j]]
                    if equip_rarity + 1 not in self.weapon_status[weapon_type]:
                        bm_upgrade_data[(i * 0x1C) + 0x10 + (2 * j):
                                        (i * 0x1C) + 0x10 + (2 * j) + 2] = struct.pack("H", 0)
                    else:
                        bm_upgrade_data[(i * 0x1C) + 0x10 + (2 * j):
                                        (i * 0x1C) + 0x10 + (2 * j) + 2] = struct.pack("H", blademaster_upgrades[i][j])
        await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang]["BLADEMASTER_UPGRADES"],
                                      bytes(bm_upgrade_data), "WRITE_UPGRADE_BM")
        gn_upgrade_data = bytearray(base64.b64decode(
            (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang]["GUNNER_UPGRADES"], 9912, "READ_UPGRADE_GN"))[
                "base64"]))
        for i in range(1, 354):
            weapon_type, equip_rarity = gunner[i]
            if weapon_type != 10:
                continue  # small optimization here, only bows use the regular upgrade system in FU
            if self.cash_only:
                gn_upgrade_data[(i * 0x1C): (i * 0x1C) + 0x10] = [0] * 16
            for j in range(6):
                if gunner_upgrades[i][j] > 0:
                    weapon_type, equip_rarity = gunner[gunner_upgrades[i][j]]
                    if equip_rarity + 1 not in self.weapon_status[weapon_type]:
                        gn_upgrade_data[(i * 0x1C) + 0x10 + (2 * j):
                                        (i * 0x1C) + 0x10 + (2 * j) + 2] = struct.pack("H", 0)
                    else:
                        gn_upgrade_data[(i * 0x1C) + 0x10 + (2 * j):
                                        (i * 0x1C) + 0x10 + (2 * j) + 2] = struct.pack("H", gunner_upgrades[i][j])
        await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang]["GUNNER_UPGRADES"],
                                      bytes(gn_upgrade_data), "WRITE_UPGRADE_GN")
        ppsspp_logger.info("Refreshed equipment status.")

    async def refresh_task(self) -> None:
        # set of initialization we need to handle first
        while not self.exit_event.is_set():
            try:
                try:
                    await asyncio.wait_for(self.watcher_event.wait(), 0.125)
                except asyncio.TimeoutError:
                    pass
                self.watcher_event.clear()
                if self.server is None or self.slot is None or self.debugger is None or self.debugger.closed:
                    continue
                if self.refresh:
                    await self.get_key_binary()
                    await self.set_equipment_status()
                    self.refresh = False
            except Exception as ex:
                Utils.messagebox("Error", str(ex), True)
                logger.error(traceback.format_exc())

    async def send_trap_link(self, item: NetworkItem) -> None:
        item_name = self.item_names.lookup_in_game(item.item)
        if not self.slot or self.slot < 0 or "TrapLink" not in self.tags or item_name not in local_trap_to_type:
            return

        self.last_trap_link = time()

        await self.send_msgs([{
            "cmd": "Bounce",
            "tags": ["TrapLink"],
            "data": {
                "time": self.last_trap_link,
                "source": self.player_names[self.slot],
                "trap_name": item_name
            },
        }])

    async def pop_item(self) -> None:
        if self.item_queue:
            item = self.item_queue.pop()
            if item.item == 24700083:
                # Zenny Bag
                current_zenny = (await self.ppsspp_read_unsigned(MHFU_POINTERS[self.lang]["ZENNY"],
                                                                 "ZENNY", 32))["value"]
                await self.ppsspp_write_unsigned(MHFU_POINTERS[self.lang]["ZENNY"],
                                                 current_zenny + 50000, "WRITE_ZENNY", 32)
            elif item.item in (24700079, 24700080):
                # Equipment
                e_type = random.choice([5, 6]) if item.item == 24700079 else random.choice(range(5))
                e_rarity_group = {1}  # always allow rare 1 items, so the items are at least useful without much
                if e_type >= 5:
                    # weapon
                    w_type = random.choice(list(self.weapon_status.keys()))
                    # now fill e_rarity with the correct value
                    e_rarity_group.update(self.weapon_status[w_type])
                    weapons = blademaster if e_type == 5 else gunner
                    e_id, e_rarity = random.choice([(idx, value[1]) for idx, value in weapons.items()
                                                    if value[1] in e_rarity_group])
                else:
                    e_rarity_group.update(self.armor_status)
                    armors = {
                        0: legs,
                        1: helms,
                        2: chests,
                        3: arms,
                        4: waists
                    }
                    e_id, e_rarity = random.choice([(idx, value) for idx, value in armors[e_type].items()
                                                    if value in e_rarity_group])
                # now read
                equipment_data = bytearray(base64.b64decode(
                    (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang]["EQUIP_CHEST"],
                                                  12000, "EQUIP_CHEST"))["base64"]))
                # each entry is a 12 byte struct, for some reason
                for i in range(1000):
                    enabled = equipment_data[i * 12]
                    if not enabled:
                        # this is a free slot we can apply our new equipment
                        equipment_data[(i * 12):i * 12 + 12] = struct.pack("BBHII", 1, e_type, e_id, 0, 0)
                        break
                else:
                    ppsspp_logger.warning("Unable to grant equipment, as equipment chest is full. Item may be lost"
                                          "if not received before disconnecting.")
                    self.item_queue.append(item)
                    return
                await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang]["EQUIP_CHEST"],
                                              bytes(equipment_data), "WRITE_EQUIP_CHEST")
            elif item.item in (24700081, 24700082):
                # item box
                i_groups = decoration_gifts if item.item == 27400081 else item_gifts
                group_name, group_info = random.choice(list(i_groups.items()))
                # get item box
                item_data = bytearray(base64.b64decode(
                    (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang]["ITEM_CHEST"], 4000, "ITEM_CHEST"))[
                        "base64"]))
                items = {i: list(struct.unpack("HH", item_data[i * 4: (i * 4) + 4])) for i in range(1000)}
                for item_id, item_num in group_info.items():
                    idx = next((item for item in items if items[item][0] == item_id), None)
                    if not idx:
                        # find the next 0 idx
                        idx = next((item for item in items if items[item][0] == 0), None)
                        if not idx:
                            continue  # this will lose the item, but we may be able to grant others
                    items[idx][0] = item_id
                    items[idx][1] += item_num
                    item_data[idx * 4: (idx * 4) + 4] = struct.pack("HH", item_id, item_num)
                await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang]["ITEM_CHEST"], item_data, "WRITE_ITEM_CHEST")
                ppsspp_logger.info(f"Received {group_name}.")
            else:
                self.item_queue.append(item)

    async def pop_trap(self) -> None:
        if self.trap_queue:
            trap = self.trap_queue.pop()
            if trap == 13:
                # Poison
                await self.ppsspp_write_unsigned(MHFU_POINTERS[self.lang]["POISON_TIMER"], 60, "POISON", 16)
            else:
                # Set Action
                await self.ppsspp_write_unsigned(MHFU_POINTERS[self.lang]["RESET_ACTION"], 1, "RESET_ACTION")
                await self.ppsspp_write_unsigned(MHFU_POINTERS[self.lang]["SET_ACTION"],
                                                 ACTIONS[trap], "SET_ACTION", 16)

    async def receive_items(self, item: NetworkItem) -> None:
        if item.item in range(24700079, 24700084):
            self.item_queue.append(item)
        elif item.item >= 24700500:
            # traps
            if self.trap_link:
                await self.send_trap_link(item)
            self.trap_queue.append(item.item - 24700500)
        elif item_id_to_name[item.item] in item_name_groups["Weapons"]:
            # there's like 50 of these gimme a break
            self.refresh = True
            local_id = item.item - base_id
            weapon_group = local_id // 11
            if weapon_group < 11:
                for weapon in WEAPON_GROUPS[weapon_group]:
                    if not local_id % 11:
                        # progressive
                        if not self.weapon_status[weapon]:
                            current_max = 0
                        else:
                            current_max = max(self.weapon_status[weapon])
                        self.weapon_status[weapon].add(current_max + 1)
                    else:
                        self.weapon_status[weapon].add(local_id % 11)
            else:
                if not local_id % 11:
                    # progressive
                    if not self.weapon_status[0]:
                        current_max = 0
                    else:
                        current_max = max(self.weapon_status[0])
                    for j in range(11):
                        self.weapon_status[j].add(current_max + 1)
                else:
                    rarity = local_id % 11
                    for j in range(11):
                        self.weapon_status[j].add(rarity)
        elif item_id_to_name[item.item] in item_name_groups["Armor"]:
            local_id = item.item - base_id - 66
            if local_id == 0:
                # progressive
                if not self.armor_status:
                    current_max = 0
                else:
                    current_max = max(self.armor_status)
                self.armor_status.add(current_max + 1)
            else:
                self.armor_status.add(local_id)
        if item.item not in range(24700079, 24700084) and item.item < 24700500:
            self.refresh = True

    def run_gui(self) -> None:
        from kvui import GameManager
        from kivymd.uix.label import MDLabel
        from kivy.uix.layout import Layout

        class MHFUManager(GameManager):
            ctx: MHFUContext
            logging_pairs = [
                ("Client", "Archipelago"),
                ("PPSSPP", "PPSSPP"),
            ]
            base_title = "Archipelago Monster Hunter Freedom Unite Client"
            keys: MDLabel | None = None

            def build(self) -> Layout:
                b = super().build()

                keys = MDLabel(text="Key Quests: 0/0",
                               size_hint_x=None, width=150)
                self.keys = keys

                self.connect_layout.add_widget(keys)
                return b

            def update_keys(self, current: int, target: int) -> None:
                if self.keys:
                    self.keys.text = f"Key Quests: {current}/{target}"

        self.ui = MHFUManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_deathlink(self, data: dict[str, Any]) -> None:
        self.last_death_link = max(data["time"], self.last_death_link)
        cause = data.get("cause", "")
        if not cause:
            logger.info(f"DeathLink: Received from {data['source']}")
        else:
            logger.info(f"DeathLink: {cause}")
        self.death_state = DeathState.killing_player

    def handle_bounce(self, args: dict[str, Any]) -> None:
        assert self.slot is not None
        if "tags" in args:
            if "TrapLink" in args["tags"]:
                source = args["source"]
                if source != self.player_names[self.slot]:
                    name = args["trap_name"]
                    if name in trap_link_matches:
                        self.trap_queue.extend([trap for trap in trap_link_matches[name]
                                                if trap in self.allowed_traps])
                    logger.info(f"TrapLink: Received {name} from {source}")

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Connected":
            # pick up our slot data
            self.death_link = args["slot_data"]["death_link"]
            self.goal = args["slot_data"]["goal"]
            self.goal_quest = goal_quests[self.goal]
            self.quest_multiplier = float(args["slot_data"]["quest_difficulty_multiplier"] / 100)
            self.quest_randomization = args["slot_data"]["quest_randomization"]
            self.quest_info = args["slot_data"]["quest_info"]
            self.cash_only = args["slot_data"]["cash_only_equipment"]
            self.set_cutscene = args["slot_data"]["set_cutscene"]
            self.trap_link = args["slot_data"]["trap_link"]
            self.allowed_traps = args["slot_data"]["allowed_traps"]
            self.required_keys = args["slot_data"]["required_keys"]
            for group, value in args["slot_data"]["rank_requirements"].items():
                hub, rank, star = group.split(",")
                self.rank_requirements[int(hub), int(rank), int(star)] = value
            # initialize certain variables
            self.recv_index = 0
            self.unlocked_keys = 0
            self.refresh = True

        elif cmd == "RoomInfo":
            self.server_seed_name = args.get("seed_name", None)
        elif cmd == "Bounced":
            self.handle_bounce(args)

    async def shutdown(self) -> None:
        await super().shutdown()
        if self.debugger and not self.debugger.closed:
            await self.debugger.close()
        if self.breakpoint_task:
            self.breakpoint_task.cancel()
        if self.watcher_task:
            self.watcher_task.cancel()
        if self.update_task:
            self.update_task.cancel()
        if self.socket_task:
            self.socket_task.cancel()


async def game_watcher(ctx: MHFUContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()
            if ctx.server is None or ctx.slot is None or ctx.debugger is None or ctx.debugger.closed:
                continue

            if ctx.death_link and "DeathLink" not in ctx.tags:
                await ctx.update_death_link(ctx.death_link > 0)

            game_status = await send_and_receive(ctx, json.dumps(PPSSPP_STATUS), "AP_STATUS")
            if not game_status["game"] or game_status["game"]["id"] not in (MHFU_SERIAL, MHP2G_SERIAL):
                ppsspp_logger.error(
                    "Connected to PPSSPP but MHFU is not currently being played. Please run /psp when MHFU is"
                    " loaded.")
                del ctx.debugger
                ctx.debugger = None
                await ctx.disconnect(False)
                continue

            current_overlay = await ctx.ppsspp_read_string(MHFU_POINTERS[ctx.lang]["CURRENT_OVL"], "CURRENT_OVL")
            if current_overlay["value"] in ("game_task.ovl", "lobby_task.ovl", "arcade_task.ovl"):
                # we have loaded a character, and are in the lobby or on a hunt

                ap_info = (await ctx.ppsspp_read_unsigned(MHFU_POINTERS[ctx.lang]["AP_SAVE"], "AP_SAVE", 32))["value"]
                assert ctx.server_seed_name is not None
                if ap_info != 0:
                    if ap_info != crc32(ctx.server_seed_name.encode("utf-8")):
                        ppsspp_logger.error("This hunter is registered to another multiworld!\n"
                                            "Please make sure you loaded the correct save.")
                        await ctx.disconnect(False)
                        continue
                else:
                    # generate a new id and save on save file
                    await ctx.ppsspp_write_unsigned(MHFU_POINTERS[ctx.lang]["AP_SAVE"],
                                                    crc32(ctx.server_seed_name.encode("utf-8")), "AP_SAVE", 32)

                ctx.recv_index = (await ctx.ppsspp_read_unsigned(MHFU_POINTERS[ctx.lang]["AP_SAVE"] + 4,
                                                                 "RECV_INDEX", 32))["value"]
                if ctx.recv_index < len(ctx.items_received):
                    await ctx.receive_items(ctx.items_received[ctx.recv_index])
                    ctx.recv_index += 1
                    await ctx.ppsspp_write_unsigned(MHFU_POINTERS[ctx.lang]["AP_SAVE"] + 4,
                                                    ctx.recv_index, "WRITE_RECV_INDEX", 32)
                old_keys = ctx.unlocked_keys
                ctx.unlocked_keys = sum(1 for item in ctx.items_received if item.item == 24700077)
                if ctx.unlocked_keys != old_keys:
                    ctx.refresh = True

                if ctx.set_cutscene:
                    cutscenes = (await ctx.ppsspp_read_unsigned(MHFU_POINTERS[ctx.lang]["NARGA_HYPNOC_CUTSCENE"],
                                                                "NARGA_HYPNOC"))["value"]
                    await ctx.ppsspp_write_unsigned(MHFU_POINTERS[ctx.lang]["NARGA_HYPNOC_CUTSCENE"], cutscenes | 0x60,
                                                    "WRITE_NARGA_HYPNOC")
                    ctx.set_cutscene = None
                await ctx.pop_item()
                if current_overlay["value"] in ("game_task.ovl", "arcade_task.ovl"):
                    # we're on a hunt, pop traps and check deathlink
                    current_action = (await ctx.ppsspp_read_unsigned(MHFU_POINTERS[ctx.lang]["SET_ACTION"],
                                                                     "CURRENT_ACTION", 16))["value"]
                    if current_action == 0x0300 and ctx.death_link == 1:
                        if ctx.death_state == DeathState.alive:
                            await ctx.send_death(f"{ctx.player_names[ctx.slot]} carted.")
                        ctx.death_state = DeathState.dead
                    else:
                        if ctx.death_link == 1:
                            if ctx.death_state == DeathState.killing_player:
                                await ctx.ppsspp_write_unsigned(MHFU_POINTERS[ctx.lang]["RESET_ACTION"], 1,
                                                                 "RESET_DEATH")
                                await ctx.ppsspp_write_unsigned(MHFU_POINTERS[ctx.lang]["SET_ACTION"],
                                                                 ACTIONS[-1], "SET_DEATH", 16)
                            else:
                                ctx.death_state = DeathState.alive
                        await ctx.pop_trap()
                else:
                    # if we're not in a hunt, we just need to reset deathlinks
                    if ctx.death_state != DeathState.alive:
                        ctx.death_state = DeathState.alive

                new_checks = []
                quest_changed = False
                completion_bytes = await ctx.ppsspp_read_bytes(MHFU_POINTERS[ctx.lang]["QUEST_COMPLETE"],
                                                               63, "QUEST_COMPLETE")
                quest_completion = bytearray(base64.b64decode(completion_bytes["base64"]))
                for idx, quest in enumerate(quest_data):
                    flag = quest["flag"]
                    mask = quest["mask"]
                    if flag >= 0 and mask >= 0:
                        if quest_completion[flag] & (1 << mask):
                            if base_id + idx not in ctx.checked_locations and base_id + idx not in ctx.locations_checked:
                                new_checks.append(idx + base_id)
                            if quest["qid"] == ctx.goal_quest and not ctx.finished_game:
                                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                                ctx.finished_game = True
                        elif base_id + idx in ctx.checked_locations:
                            quest_changed = True
                            quest_completion[flag] |= (1 << mask)
                if quest_changed:
                    await ctx.ppsspp_write_bytes(MHFU_POINTERS[ctx.lang]["QUEST_COMPLETE"],
                                                 bytes(quest_completion), "WRITE_QUEST_COMPLETE")

                treasure_score = struct.unpack("IIIIIII",
                                               base64.b64decode((await ctx.ppsspp_read_bytes(MHFU_POINTERS[ctx.lang][
                                                                                                 "TREASURE_SCORE"],
                                                                                             28, "TREASURE")
                                                                 )["base64"]))
                for score, t_quest in zip(treasure_score, (f"m0400{i}" for i in range(1, 8))):
                    silver, gold = TREASURE_SCORES[t_quest]
                    if score >= silver:
                        quest_name = get_proper_name(get_quest_by_id(t_quest))
                        silver_id = location_name_to_id[f"{quest_name} - Silver Crown"]
                        if silver_id not in ctx.checked_locations:
                            new_checks.append(silver_id)
                        if score >= gold:
                            gold_id = location_name_to_id[f"{quest_name} - Gold Crown"]
                            if gold_id not in ctx.checked_locations:
                                new_checks.append(gold_id)

                if new_checks:
                    for new_check_id in new_checks:
                        ctx.locations_checked.add(new_check_id)
                        location = ctx.location_names.lookup_in_game(new_check_id)
                        ppsspp_logger.info(
                            f'New Check: {location} ({len(ctx.locations_checked)}/'
                            f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.check_locations(new_checks)
        except Exception as ex:
            Utils.messagebox("Error", str(ex), True)
            logger.error(traceback.format_exc())


async def main(args: "argparse.Namespace") -> None:
    ctx = MHFUContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    ctx.socket_task = asyncio.create_task(receive_all(ctx), name="ReceiveAll")
    await connect_psp(ctx)
    ctx.breakpoint_task = asyncio.create_task(handle_logs(ctx), name="LogHandler")
    ctx.watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")
    ctx.update_task = asyncio.create_task(ctx.refresh_task(), name="UpdateTask")
    await ctx.exit_event.wait()
    if ctx.debugger and not ctx.debugger.closed:
        await ctx.debugger.close()
    await ctx.shutdown()


def launch(*launch_args: str) -> None:
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
