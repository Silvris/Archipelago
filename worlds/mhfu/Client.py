from __future__ import annotations

import random
import typing

from kivy.uix.label import Label
from operator import itemgetter
import Utils
import logging
from CommonClient import CommonContext, ClientCommandProcessor, gui_enabled, get_base_parser, server_loop
import asyncio
from websockets import client
import base64
import json
import struct

from NetUtils import NetworkItem, ClientStatus
from .Quests import quest_data, base_id, goal_quests
from .Items import item_name_to_id, item_id_to_name, item_name_groups
from .data.Monsters import elder_dragons
from .data.Equipment import blademaster, gunner, blademaster_upgrades, gunner_upgrades, \
    helms, chests, arms, waists, legs

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
        "ZENNY": 0x099FF090,
        "CURRENT_OVL": 0x09A5A5A0,
        "RESET_ACTION": 0x090AF355,  # byte
        "SET_ACTION": 0x090AF418,  # half
        "FAIL_QUEST": 0x09A01B1C,  # byte
        "POISON_TIMER": 0x090AF508  # half
    }
}

MHFU_BREAKPOINTS = {
    # logFormat: memory, address, size, enabled, log, read, write, change
    # enabled being "do we want to pause emulation here"
    # disabled effectively acting as an event system
    # memory being this is a memory breakpoint, else it's CPU
    # CPU breakpoints don't use read/write/change
    "QUEST_LOAD": (True, 0x08A57510, 1, True, True, True, False, False),
    "QUEST_COMPLETE": (True, 0x09999DC8, 63, False, True, False, True, True),
    "MONSTER_LOAD": (False, 0x08871C24, 1, True, True, False, False, False),
    #"MONSTER_LOAD_RESPAWN": (False, 0x09B18F10, 1, True, True, False, False, False)
}

MHFU_BREAKPOINT_ARGS = {
    # do this so we can just pass the former directly, while parse this one
    # this lets us pull register info from the breakpoint
    "MONSTER_LOAD": ["{a0}"],
    #"MONSTER_LOAD_RESPAWN": ["{s2}"],
}

ACTIONS = {
    -1: 0x0300,  # Kill Player
    10: 0x0072,  # Farcaster
    11: 0x0215,  # Sleep
    12: 0x0216,  # Paralysis
    13: 0x021B,  # Snowman
    14: 0x0019,  # Use Item
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
    4: [1, 5, 10]
}


async def handle_logs(ctx: MHFUContext, logs: typing.List):
    checked_quests = False
    for log in logs:
        if log["channel"] in ("MEMMAP", "JIT"):
            # we hit a breakpoint
            breakpoint = log["message"].replace("\n", "").rsplit(" ")[-1]
            print(breakpoint)
            if breakpoint == "QUEST_LOAD":
                if ctx.randomize_quest:
                    quest_base = MHFU_BREAKPOINTS[breakpoint][1]
                    quest_id = (await ctx.ppsspp_read_unsigned(quest_base + 100, 16))["value"]
                    large_mon_ptr_ptr = quest_base + 0x14
                    large_mon_ptr = (await ctx.ppsspp_read_unsigned(large_mon_ptr_ptr, 32))["value"]
                    large_mon_id_ptr = await ctx.ppsspp_read_unsigned(large_mon_ptr + quest_base + 8, 32)
                    large_mon_info_ptr = await ctx.ppsspp_read_unsigned(large_mon_ptr + 12 + quest_base, 32)
                    large_mons = struct.unpack("IIII",
                                               base64.b64decode((await ctx.ppsspp_read_bytes(
                                                   large_mon_id_ptr["value"] + quest_base, 16))["base64"]))
                    mons = {}
                    for idx, mon in enumerate([mon for mon in large_mons if mon != 0xFFFFFFFF]):
                        # pull the mons
                        mons[idx] = await ctx.ppsspp_read_bytes(large_mon_info_ptr["value"] + quest_base + (idx * 60),
                                                                60)
                    print(mons)
                    # apply difficulty modifier
                    if mons and ctx.quest_randomization:
                        info_out = bytearray()
                        quest_mons = ctx.quest_monsters[str("%.5i" % quest_id)]
                        for mon in mons:
                            mon_data = bytearray(base64.b64decode(mons[mon]["base64"]))
                            if ctx.quest_randomization:
                                mon_data[0:4] = struct.pack("I", quest_mons[mon])
                            info_out.extend(mon_data)
                        await ctx.ppsspp_write_bytes(large_mon_info_ptr["value"] + quest_base, info_out)
                        # need to write new monster ids
                        await ctx.ppsspp_write_bytes(large_mon_id_ptr["value"] + quest_base,
                                                         struct.pack("IIII", *quest_mons,
                                                                     *[0xFFFFFFFF] * (4 - len(quest_mons))))
                        # now pick one to be the quest target
                        target_mon = random.choice(quest_mons)
                        quest_mons.remove(target_mon)
                        await ctx.ppsspp_write_bytes(quest_base + 0x70,
                                                         struct.pack("HH", target_mon, 1))
                        if quest_mons and random.random() > 0.5:
                            # secondary goal
                            target_mon = random.choice(quest_mons)
                            quest_mons.remove(target_mon)
                            await ctx.ppsspp_write_bytes(quest_base + 0x78,
                                                         struct.pack("HH", target_mon, 1))
                        else:
                            # need to null these 3
                            await ctx.ppsspp_write_bytes(quest_base + 0x78, struct.pack("HH", 0, 0))
                # this gets pinged twice during quest load, we edit the first and fall through the second
                ctx.randomize_quest = not ctx.randomize_quest
            elif "MONSTER_LOAD" in breakpoint:
                breakpoint, mon_addr = breakpoint.split("|")
                mon_address = int(mon_addr, 16)
                health = (await ctx.ppsspp_read_unsigned(mon_address + 0x2E4, 16))["value"]
                health = min(max(int(health * ctx.quest_multiplier), 1), 0xFFFF)
                await ctx.ppsspp_write_unsigned(mon_address + 0x2E4, health, 16)
                await ctx.ppsspp_write_unsigned(mon_address + 0x41E, health, 16)

            elif breakpoint == "QUEST_COMPLETE":
                # ~400 of this type get sent on every quest completion
                # madness, we have to clear some of them
                if checked_quests:
                    continue
                new_checks = []
                completion_bytes = await ctx.ppsspp_read_bytes(MHFU_POINTERS[ctx.lang]["QUEST_COMPLETE"], 63)
                quest_completion = bytearray(base64.b64decode(completion_bytes["base64"]))
                for id, quest in enumerate(quest_data):
                    flag = int(quest["flag"])
                    mask = int(quest["mask"])
                    if flag >= 0 and mask >= 0:
                        if quest_completion[flag] & (1 << mask):
                            if base_id + id not in ctx.checked_locations:
                                new_checks.append(id + base_id)
                            if id == ctx.goal_quest and not ctx.finished_game:
                                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                                ctx.finished_game = True
                        elif base_id + id in ctx.checked_locations:
                            quest_completion[flag] |= (1 << mask)
                await ctx.ppsspp_write_bytes(MHFU_POINTERS[ctx.lang]["QUEST_COMPLETE"], bytes(quest_completion))

                if new_checks:
                    for new_check_id in new_checks:
                        ctx.locations_checked.add(new_check_id)
                        location = ctx.location_names[new_check_id]
                        ppsspp_logger.info(
                            f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

                checked_quests = True

            if MHFU_BREAKPOINTS[breakpoint][3]:
                # this break point stops emulation, we need to restart it
                await send_and_receive(ctx, json.dumps({"event": "cpu.resume"}), "cpu.resume")


async def receive_all(ctx: MHFUContext):
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
    regular, logs = [], []
    for x in results:
        (regular, logs)[x["event"] == "log"].append(x)
    await handle_logs(ctx, logs)
    return regular


async def send_and_receive(ctx: MHFUContext, message: str, event: str):
    # since we can't register for a specific change in value,
    # we can just wait until we receive the one we're looking for
    await ctx.debugger.send(message)
    results = await receive_all(ctx)
    logs = [message for message in results if message["event"] == "log"]
    if logs:
        print(logs)
    return next((message for message in results if message["event"] == event), None)


async def connect_psp(ctx: MHFUContext, target: typing.Optional[int] = None):
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
    for breakpoint in MHFU_BREAKPOINTS:
        if MHFU_BREAKPOINTS[breakpoint][0]:
            response = await send_and_receive(ctx, json.dumps(
                dict(zip(["event", "address", "size", "enabled", "log", "read", "write", "change", "logFormat"],
                         ["memory.breakpoint.add", *MHFU_BREAKPOINTS[breakpoint][1:],
                          '|'.join([breakpoint, *MHFU_BREAKPOINT_ARGS.get(breakpoint, list())])]
                         ))), "memory.breakpoint.add")
        else:
            response = await send_and_receive(ctx, json.dumps(
                dict(zip(
                    ["event", "address", "enabled", "log", "logFormat"],
                    ["cpu.breakpoint.add", MHFU_BREAKPOINTS[breakpoint][1], MHFU_BREAKPOINTS[breakpoint][3],
                     MHFU_BREAKPOINTS[breakpoint][4], '|'.join([breakpoint, *MHFU_BREAKPOINT_ARGS.get(breakpoint, list())])]
                ))
            ), "cpu.breakpoint.add")
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
    want_slot_data = True

    # game info
    recv_index = -1
    death_link = False
    goal: int = 0
    goal_quest: int = 3233  # This is Ukanlos, pick the furthest out to potentially avoid collision
    unlocked_keys: int = 0
    required_keys: int = 0
    refresh: bool = False
    rank_requirements: typing.Dict[(int, int, int), int] = {}
    weapon_status: typing.Dict[int, typing.Set[int]] = {
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
    armor_status: typing.Set[int] = set()
    quest_randomization: bool = False
    quest_monsters: typing.Dict[str, typing.List[int]]
    quest_multiplier: float = 1.0
    cash_only: bool = False
    item_queue: typing.List[NetworkItem] = []

    # intermitten
    randomize_quest: bool = True

    async def ppsspp_read_bytes(self, offset, length):
        result = await send_and_receive(self, json.dumps({
            "event": "memory.read",
            "address": offset,
            "size": length
        }), "memory.read")
        return result

    async def ppsspp_read_unsigned(self, offset, length=8):
        if length not in (8, 16, 32):
            raise Exception("Can only read 8/16/32-bit integers.")
        result = await send_and_receive(self, json.dumps({
            "event": f"memory.read_u{length}",
            "address": offset
        }), f"memory.read_u{length}")
        return result

    async def ppsspp_read_string(self, offset):
        result = await send_and_receive(self, json.dumps({
            "event": "memory.readString",
            "address": offset
        }), "memory.readString")
        return result

    async def ppsspp_write_bytes(self, offset, data):
        result = await send_and_receive(self, json.dumps({
            "event": "memory.write",
            "address": offset,
            "base64": str(base64.b64encode(data), "utf-8")
        }), "memory.write")
        return result

    async def ppsspp_write_unsigned(self, offset, value, length=8):
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

    async def get_key_binary(self):
        target = 65535
        for hub, rank, star in sorted(self.rank_requirements, key=itemgetter(0, 1, 2)):
            if (hub, rank, star) in KEY_OFFSETS:
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
                await self.ppsspp_write_bytes(address, data)
        if self.ui:
            self.ui.update_keys(self.unlocked_keys, target)

    async def set_equipment_status(self):
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
                (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang][equip_group], length))["base64"]))
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
            await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang][equip_group], bytes(create_data))

        bm_upgrade_data = bytearray(base64.b64decode(
            (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang]["BLADEMASTER_UPGRADES"], 32200))["base64"]))
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
        await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang]["BLADEMASTER_UPGRADES"], bytes(bm_upgrade_data))
        gn_upgrade_data = bytearray(base64.b64decode(
            (await self.ppsspp_read_bytes(MHFU_POINTERS[self.lang]["GUNNER_UPGRADES"], 9912))["base64"]))
        for i in range(1, 354):
            if self.cash_only:
                gn_upgrade_data[(i * 0x1C): (i * 0x1C) + 0x10] = [0] * 16
            weapon_type, equip_rarity = gunner[i]
            if weapon_type != 10:
                continue  # small optimization here, only bows use the regular upgrade system in FU
            for j in range(6):
                if gunner_upgrades[i][j] > 0:
                    weapon_type, equip_rarity = gunner[gunner_upgrades[i][j]]
                    if equip_rarity + 1 not in self.weapon_status[weapon_type]:
                        gn_upgrade_data[(i * 0x1C) + 0x10 + (2 * j):
                                        (i * 0x1C) + 0x10 + (2 * j) + 2] = struct.pack("H", 0)
                    else:
                        gn_upgrade_data[(i * 0x1C) + 0x10 + (2 * j):
                                        (i * 0x1C) + 0x10 + (2 * j) + 2] = struct.pack("H", gunner_upgrades[i][j])
        await self.ppsspp_write_bytes(MHFU_POINTERS[self.lang]["GUNNER_UPGRADES"], bytes(gn_upgrade_data))
        ppsspp_logger.info("Refreshed equipment status.")

    async def connect_init(self):
        # set of initialization we need to handle first
        await self.get_key_binary()
        await self.set_equipment_status()

    async def pop_item(self):
        if self.item_queue:
            item = self.item_queue.pop()

            if item.item == 24700083:
                # Zenny Bag
                current_zenny = (await self.ppsspp_read_unsigned(MHFU_POINTERS[self.lang]["ZENNY"]))["value"]
                await self.ppsspp_write_unsigned(MHFU_POINTERS[self.lang]["ZENNY"], current_zenny + 50000, 16)
            else:
                self.item_queue.append(item)

    def receive_items(self, items: typing.List[NetworkItem]):
        # we might need to come up with a data storage solution for weapon/armor gifts, but for now, grant always
        for item in items:
            if item.item == 24700077:
                # Key Quest
                self.unlocked_keys += 1
            elif item.item in range(24700079, 24700084):
                # Can only handle these in specific ovls
                self.item_queue.append(item)
            elif item_id_to_name[item.item] in item_name_groups["Weapons"]:
                # there's like 50 of these gimme a break
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
                        for i in range(11):
                            self.weapon_status[i].add(current_max + 1)
                    else:
                        rarity = local_id % 11
                        for i in range(11):
                            self.weapon_status[i].add(rarity)
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
        self.refresh = True
        self.recv_index = len(items)

    def run_gui(self):
        from kvui import GameManager

        class MHFUManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("PPSSPP", "PPSSPP"),
            ]
            base_title = "Archipelago Monster Hunter Freedom Unite Client"
            keys: typing.Optional[Label] = None

            def build(self):
                b = super().build()

                keys = Label(text="Key Quests: 0/0",
                             size_hint_x=None, width=150)
                self.keys = keys

                self.connect_layout.add_widget(keys)
                return b

            def update_keys(self, current, target):
                if self.keys:
                    self.keys.text = f"Key Quests: {current}/{target}"

        self.ui = MHFUManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            # pick up our slot data
            self.death_link = args["slot_data"]["death_link"]
            self.goal = args["slot_data"]["goal"]
            self.goal_quest = int(goal_quests[self.goal][1:])
            self.quest_multiplier = float(args["slot_data"]["quest_difficulty_multiplier"] / 100)
            self.quest_randomization = args["slot_data"]["quest_randomization"]
            self.quest_monsters = args["slot_data"]["quest_monsters"]
            self.cash_only = args["slot_data"]["cash_only_equipment"]
            self.required_keys = args["slot_data"]["required_keys"]
            for group, value in args["slot_data"]["rank_requirements"].items():
                hub, rank, star = group.split(",")
                self.rank_requirements[int(hub), int(rank), int(star)] = value
            # initialize certain variables
            self.recv_index = -1
            self.unlocked_keys = 0
            self.refresh = True
        elif cmd == "ReceivedItems":
            self.receive_items(args["items"])


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

            if ctx.refresh:
                await ctx.get_key_binary()
                await ctx.set_equipment_status()
                ctx.refresh = False

            current_overlay = await ctx.ppsspp_read_string(MHFU_POINTERS[ctx.lang]["CURRENT_OVL"])
            if current_overlay["value"] in ("game_task.ovl", "lobby_task.ovl"):
                # we have loaded a character, and are in the lobby or on a hunt
                await ctx.pop_item()
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
