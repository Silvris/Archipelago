import logging
import random
import time
from enum import IntEnum
from base64 import b64encode
from typing import TYPE_CHECKING, Any

import Utils
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient
from MultiServer import mark_raw
from Utils import get_unique_identifier

from .data.pokemon import egg_groups, special_encounters
from .names import POKEDEX, POKEDEX_INVERSE
from .regions import shops_by_board

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

gba_logger = logging.getLogger("GBA")
logger = logging.getLogger("Client")

PINBALL_MAIN = 0x200B0C0
PINBALL_EREADER = PINBALL_MAIN + 0x7  # size 0x05
PINBALL_POKEDEX = PINBALL_MAIN + 0x74  # Size 0xCD
PINBALL_HIGH_SCORES = PINBALL_MAIN + 0x158  # Size 0x17F

PINBALL_CURRENT = 0x2000000  # It can technically be different, but in reality it never is
PINBALL_LIVES = PINBALL_CURRENT + 0x30
PINBALL_SCORE_ADD = PINBALL_CURRENT + 0x40  # size 4, used to add score
PINBALL_SCORE = PINBALL_CURRENT + 0x44  # size 4 + 4 (see score info for goaling)
PINBALL_FORCE_SPECIAL = PINBALL_CURRENT + 0x12B
PINBALL_FORCE_PICHU = PINBALL_CURRENT + 0x12C
PINBALL_COINS = PINBALL_CURRENT + 0x192
PINBALL_COIN_AWARD = PINBALL_CURRENT + 0x194
PINBALL_COIN_TIMER = PINBALL_CURRENT + 0x196  # size 2
PINBALL_SAVER = PINBALL_CURRENT + 0x724  # size 2

PINBALL_AP_START = 0x2033000
PINBALL_STARTING_LIVES = PINBALL_AP_START
PINBALL_STARTING_COINS = PINBALL_AP_START + 1
PINBALL_STARTING_BALL = PINBALL_AP_START + 2
PINBALL_PICHU_UPGRADE = PINBALL_AP_START + 3
PINBALL_COIN_MODIFIER = PINBALL_AP_START + 4
PINBALL_BOARDS = PINBALL_AP_START + 5
PINBALL_SFX = PINBALL_AP_START + 6  # size 2
PINBALL_GET = PINBALL_AP_START + 8
PINBALL_EVO = PINBALL_AP_START + 9
PINBALL_HATCH = PINBALL_AP_START + 10
PINBALL_RECEIVED = PINBALL_AP_START + 11  # size 2
PINBALL_BONUS = PINBALL_AP_START + 13
PINBALL_COIN = PINBALL_AP_START + 14
PINBALL_MEDALS = PINBALL_AP_START + 15
PINBALL_STAGES = PINBALL_AP_START + 0x10  # Size 14
PINBALL_EGGS = PINBALL_AP_START + 0x20  # Size 4
PINBALL_EVO_ITEMS = PINBALL_AP_START + 0x24
PINBALL_HELPERS = PINBALL_AP_START + 0x26  # size 1
PINBALL_DEXNAV = PINBALL_AP_START + 0x27
PINBALL_RUBY_BUMPER = PINBALL_AP_START + 0x28
PINBALL_SAPPHIRE_BUMPER = PINBALL_AP_START + 0x29
PINBALL_RUBY_BALL_UPGRADE = PINBALL_AP_START + 0x2A
PINBALL_SAPPHIRE_BALL_UPGRADE = PINBALL_AP_START + 0x2B
PINBALL_MAKUHITA_BALL_UPGRADE = PINBALL_AP_START + 0x2C
PINBALL_RINGLINK_PACKET_GAIN = PINBALL_AP_START + 0x2D
PINBALL_RINGLINK_PACKET_LOSS = PINBALL_AP_START + 0x2E
PINBALL_GOAL_CHECK = PINBALL_AP_START + 0x2F
PINBALL_SHOPS = PINBALL_AP_START + 0x31
PINBALL_ROULETTES = PINBALL_AP_START + 0x3B
PINBALL_DEATHLINK_RECV = PINBALL_AP_START + 0x40
PINBALL_DEATHLINK_SEND = PINBALL_AP_START + 0x42
PINBALL_ALWAYS_OPEN_SHOP = PINBALL_AP_START + 0x43

PINBALL_STR_MODE = 0x2035100
PINBALL_STR_ITEM = PINBALL_STR_MODE + 4
PINBALL_STR_PLAYER = PINBALL_STR_MODE + 8

PINBALL_NAME = 0x6BC000
PINBALL_VERSION = 0x6BC020
PINBALL_SLOT_INFO = 0x6BC024
PINBALL_GOAL = 0x6BC030
PINBALL_DEX_REQ = 0x6BC032
PINBALL_SCORE_REQ = 0x6BC034
PINBALL_TARGET_REQ = 0x6BC03C
PINBALL_MEDAL_REQ = 0x6BC056
PINBALL_TRIGGER_REQ = 0x6BC057
PINBALL_SHOP_MAX = 0x6BC058
PINBALL_SHOP_CHECK_MAX = 0x6BC059
PINBALL_ROULETTE_MAX = 0x6BC05A
PINBALL_DEATHLINK = 0x6BC05B


EREADER_MAP: dict[str, tuple[int, int]] = {
    "Special Guests": (0, 7),
    "Encounter Rate Up": (1, 8),
    "Ruins Area": (3, 9),
}

EREADER_MAP_INVERSE: dict[int, str] = {
    data[0]: card for card, data in EREADER_MAP.items()
}

DEBUG = False  # Debug flag

@mark_raw
def cmd_ereader(self: "BizHawkClientCommandProcessor", card: str) -> None:
    """Activate a received e-Reader card."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Pokemon Pinball Ruby & Sapphire":
        logger.warning("This command can only be used when playing Pokemon Pinball Ruby & Sapphire.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    assert isinstance(self.ctx, BizHawkClientContext)
    assert isinstance(self.ctx.client_handler, PinballRSClient)
    client: PinballRSClient = self.ctx.client_handler

    if card.title() not in EREADER_MAP:
        logger.warning(f"{card.title()} is not a valid E-Reader card.")
        return
    if not client.has_item(self.ctx, EREADER_MAP[card.title()][1]):
        logger.warning(f"You have not received the {card.title()} E-Reader card.")
        return
    client.active_ereader = EREADER_MAP[card.title()][0]


def cmd_high_scores(self: "BizHawkClientCommandProcessor"):
    """"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Pokemon Pinball Ruby & Sapphire":
        logger.warning("This command can only be used when playing Pokemon Pinball Ruby & Sapphire.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    assert isinstance(self.ctx, BizHawkClientContext)
    assert isinstance(self.ctx.client_handler, PinballRSClient)
    client: PinballRSClient = self.ctx.client_handler
    client.print_scores = True


def cmd_dexnav(self: "BizHawkClientCommandProcessor", pokemon: str):
    """Spend 30 (60 for rare Pokémon) to guarantee a Pokémon will appear in a location it can appear."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Pokemon Pinball Ruby & Sapphire":
        logger.warning("This command can only be used when playing Pokemon Pinball Ruby & Sapphire.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    assert isinstance(self.ctx, BizHawkClientContext)
    assert isinstance(self.ctx.client_handler, PinballRSClient)
    client: PinballRSClient = self.ctx.client_handler

    client.dexnav = POKEDEX.get(pokemon.title(), -1)


def cmd_check_goal(self: "BizHawkClientCommandProcessor"):
    """Print goal requirements for Pokémon Pinball Ruby & Sapphire."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Pokemon Pinball Ruby & Sapphire":
        logger.warning("This command can only be used when playing Pokemon Pinball Ruby & Sapphire.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    assert isinstance(self.ctx, BizHawkClientContext)
    assert isinstance(self.ctx.client_handler, PinballRSClient)
    client: PinballRSClient = self.ctx.client_handler
    client.print_goal = True


def get_sfx_write(sfx: int) -> tuple[int, bytes, str]:
    return PINBALL_SFX, sfx.to_bytes(2, 'little'), "System Bus"


def get_coin_give_write(coins: int) -> list[tuple[int, bytes, str]]:
    return [
        (PINBALL_COIN_AWARD, coins.to_bytes(1, "little"), "System Bus"),
        (PINBALL_COIN_TIMER, int.to_bytes(0, 2, "little"), "System Bus"),
    ]


def compress_pokedex(pokedex: bytes) -> int:
    val = 0
    for i in range(len(pokedex)):
        if pokedex[i] == 4:
            val |= 1 << i
    return val


def decompress_pokedex(pokedex: int) -> bytearray:
    val = bytearray(205)
    for i in range(205):
        if pokedex & (1 << i):
            val[i] = 4
    return val


class PinballRSClient(BizHawkClient):
    game = "Pokemon Pinball Ruby & Sapphire"
    system = "GBA"
    patch_suffix = ".appbrs"
    item_queue: list[NetworkItem] = []
    rom: bytes | None = None
    active_ereader: int = -1
    print_scores: bool = False
    print_goal: bool = False
    dexnav: int | None = None
    ringlink_incoming: int = 0
    ringlink_id: float | None = None
    pokedex_key: str | None = None
    pending_death_link: bool = False
    last_death_link: float = 0.0

    message_queue: list[tuple[int, int]] = []

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read, get_memory_size
        from . import PokemonPinballRSWorld

        try:
            if (await get_memory_size(ctx.bizhawk_ctx, "ROM")) < 0x700000:
                if "ereader" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("ereader")
                if "high_scores" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("high_scores")
                if "dexnav" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("dexnav")
                return False

            game_name, version = (await read(ctx.bizhawk_ctx, [(0x6BC000, 32, "ROM"),
                                                               (0x6BC020, 3, "ROM")]))
            if game_name[:4] != b"PBRS" or version != bytes(PokemonPinballRSWorld.world_version):
                if game_name[:4] == b"PBRS":
                    # I think this is an easier check than the other?
                    older_version = f"{version[0]}.{version[1]}.{version[2]}"
                    logger.warning(f"This Pokémon Pinball Ruby & Sapphire patch was generated for an different version "
                                   f"of the apworld. Please use that version to connect instead.\n"
                                   f"Patch version: ({older_version})\n"
                                   f"Client version: ({'.'.join([str(i) for i in PokemonPinballRSWorld.world_version])})")
                if "ereader" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("ereader")
                if "high_scores" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("high_scores")
                if "dexnav" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("dexnav")
                if "check_goal" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("check_goal")
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        self.rom = game_name
        ctx.items_handling = 0b111
        ctx.want_slot_data = False

        if "ereader" not in ctx.command_processor.commands:
            ctx.command_processor.commands["ereader"] = cmd_ereader
        if DEBUG and "high_score" not in ctx.command_processor.commands:
            ctx.command_processor.commands["high_score"] = cmd_high_scores
        if "dexnav" not in ctx.command_processor.commands:
            ctx.command_processor.commands["dexnav"] = cmd_dexnav
        if "check_goal" not in ctx.command_processor.commands:
            ctx.command_processor.commands["check_goal"] = cmd_check_goal

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Bounced":
            if "RingLink" in args.get("tags", []):
                data = args.get("data", {})
                if data.get("source", 0) != self.ringlink_id:
                    self.ringlink_incoming += data.get("amount", 0)
            elif "DeathLink" in args.get("tags", []):
                data = args.get("data", {})
                if data.get("time", time.time()) != self.last_death_link:
                    self.on_deathlink(ctx)

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.last_death_link = ctx.last_death_link
        await ctx.send_death(f"{ctx.player_names[ctx.slot]} is bad at pinball.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    @staticmethod
    def has_item(ctx: "BizHawkClientContext", idx: int):
        return any(item.item == idx for item in ctx.items_received)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            from worlds._bizhawk import read, write, guarded_write

            if ctx.server is None:
                return

            if ctx.slot is None:
                return

            if self.ringlink_id is None:
                self.ringlink_id = time.time()

            if self.pokedex_key is None:
                self.pokedex_key = f"PINBALLRS_POKEDEX_{ctx.team}_{ctx.slot}"
                ctx.set_notify(self.pokedex_key)
                await ctx.send_msgs([{"cmd": "Set", "key": self.pokedex_key, "default": [], "operations": [
                    {"operation": "update", "value": []}
                ]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [self.pokedex_key]}])

            # get our relevant bytes
            (local_dex, high_scores, starting_lives, starting_coins, starting_ball, pichu_upgrade, coins, medals,
                boards, get_arrows, evo_arrows, hatch_mode, coin_arrows, coin_mod, stages, items_received, local_eggs,
                e_reader, bonus_stages, current_score, current_balls, evo_items, ruby_bumper, sapphire_bumper,
                ruby_ball_upgrade, sapphire_ball_upgrade, maku_ball_upgrade, coin_plus, coin_minus, goal_check, shops,
                roulettes, deathlink_send, msg_mode, helpers, open_shop, goal, dex_req, score_req, target_req, medal_req,
             trigger, slot_info, shop_tracks, shop_len, roulette_len, deathlink_enable) = await read(ctx.bizhawk_ctx,
                [
                    (PINBALL_POKEDEX, 205, "System Bus"),
                    (PINBALL_HIGH_SCORES, 0x180, "System Bus"),
                    (PINBALL_STARTING_LIVES, 1, "System Bus"),
                    (PINBALL_STARTING_COINS, 1, "System Bus"),
                    (PINBALL_STARTING_BALL, 1, "System Bus"),
                    (PINBALL_PICHU_UPGRADE, 1, "System Bus"),
                    (PINBALL_COINS, 1, "System Bus"),
                    (PINBALL_MEDALS, 1, "System Bus"),
                    (PINBALL_BOARDS, 1, "System Bus"),
                    (PINBALL_GET, 1, "System Bus"),
                    (PINBALL_EVO, 1, "System Bus"),
                    (PINBALL_HATCH, 1, "System Bus"),
                    (PINBALL_COIN, 1, "System Bus"),
                    (PINBALL_COIN_MODIFIER, 1, "System Bus"),
                    (PINBALL_STAGES, 14, "System Bus"),
                    (PINBALL_RECEIVED, 2, "System Bus"),
                    (PINBALL_EGGS, 4, "System Bus"),
                    (PINBALL_EREADER, 5, "System Bus"),
                    (PINBALL_BONUS, 1, "System Bus"),
                    (PINBALL_SCORE, 8, "System Bus"),
                    (PINBALL_LIVES, 1, "System Bus"),
                    (PINBALL_EVO_ITEMS, 4, "System Bus"),
                    (PINBALL_RUBY_BUMPER, 1, "System Bus"),
                    (PINBALL_SAPPHIRE_BUMPER, 1, "System Bus"),
                    (PINBALL_RUBY_BALL_UPGRADE, 1, "System Bus"),
                    (PINBALL_SAPPHIRE_BALL_UPGRADE, 1, "System Bus"),
                    (PINBALL_MAKUHITA_BALL_UPGRADE, 1, "System Bus"),
                    (PINBALL_RINGLINK_PACKET_GAIN, 1, "System Bus"),
                    (PINBALL_RINGLINK_PACKET_LOSS, 1, "System Bus"),
                    (PINBALL_GOAL_CHECK, 1, "System Bus"),
                    (PINBALL_SHOPS, 10, "System Bus"),
                    (PINBALL_ROULETTES, 2, "System Bus"),
                    (PINBALL_DEATHLINK_SEND, 1, "System Bus"),
                    (PINBALL_STR_MODE, 1, "System Bus"),
                    (PINBALL_HELPERS, 1, "System Bus"),
                    (PINBALL_ALWAYS_OPEN_SHOP, 1, "System Bus"),
                    (PINBALL_GOAL, 1, "ROM"),
                    (PINBALL_DEX_REQ, 1, "ROM"),
                    (PINBALL_SCORE_REQ, 8, "ROM"),
                    (PINBALL_TARGET_REQ, 26, "ROM"),
                    (PINBALL_MEDAL_REQ, 1, "ROM"),
                    (PINBALL_TRIGGER_REQ, 1, "ROM"),
                    (PINBALL_SLOT_INFO, 1, "ROM"),
                    (PINBALL_SHOP_MAX, 1, "ROM"),
                    (PINBALL_SHOP_CHECK_MAX, 1, "ROM"),
                    (PINBALL_ROULETTE_MAX, 1, "ROM"),
                    (PINBALL_DEATHLINK, 1, "ROM"),
                ])

            if slot_info[0] & 0x2 and "RingLink" not in ctx.tags:
                ctx.tags.add("RingLink")
                await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

            if deathlink_enable[0] and "DeathLink" not in ctx.tags:
                ctx.tags.add("DeathLink")
                await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

            if self.print_scores:
                for idx, i in enumerate(range(0, len(high_scores), 24)):
                    score_lo = int.from_bytes(high_scores[i+20:i+24], "little")
                    score_hi = int.from_bytes(high_scores[i+16:i+20], "little")
                    # score_lo is capped at 99,999,999. We should be below that, but cap it if we are above
                    score = min(score_lo, 99999999) + (score_hi * 100000000)
                    logger.warning(f"Score {idx}: {score}")
                c_score = (min(int.from_bytes(current_score[:4], "little"), 99999999)
                           + (int.from_bytes(current_score[4:8], "little") * 100000000))
                logger.warning(f"Current score: {c_score}")
                self.print_scores = False

            if self.print_goal:
                trigger_types = {
                    0: "End of Ball",
                    1: "Groudon/Kyogre",
                    2: "Rayquaza",
                }
                goal_value = goal[0]
                if goal_value & 0x1:
                    # dex num
                    caught = sum(i == 4 for i in local_dex)
                    logger.warning(f"Pokédex Requirement: {caught}/{int.from_bytes(dex_req, 'little')}")
                if goal_value & 0x2:
                    # score
                    score_lo = int.from_bytes(score_req[:4], "little")
                    score_hi = int.from_bytes(score_req[4:], "little")
                    score = min(score_lo, 99999999) + (score_hi * 100000000)
                    logger.warning(f"Score Requirement: {score}")
                if goal_value & 0x4:
                    # dex targets
                    targets = int.from_bytes(target_req, "little")
                    target_strs = []
                    for i in range(205):
                        if (1 << i) & targets:
                            caught = local_dex[i] == 4
                            target_strs.append(f"{POKEDEX_INVERSE[i]}: {'Caught' if caught else 'Uncaught'}")
                    target_str = "\n".join(target_strs)
                    logger.warning(f"Target Requirement:\n {target_str}")
                if goal_value & 0x8:
                    # medals
                    logger.warning(f"Medal Requirement: {int.from_bytes(medals, 'little')}/"
                                   f"{int.from_bytes(medal_req, 'little')}")
                logger.warning(f"Goal Trigger: {trigger_types.get(trigger[0], 'Unknown')}")
                self.print_goal = False

            if not ctx.finished_game and goal_check[0] != 0:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
            writes = []

            write_local_dex = bytearray(local_dex)
            writing_dex = False

            local_ereader = bytearray(e_reader)
            if self.active_ereader > -1:
                local_ereader[self.active_ereader] = 0 if local_ereader[self.active_ereader] else 1
                logger.warning(f"{EREADER_MAP_INVERSE[self.active_ereader]} has been "
                               f"{'activated' if local_ereader[self.active_ereader] else 'deactivated'}.")
                self.active_ereader = -1

            if bytes(local_ereader) != e_reader:
                writes.append((PINBALL_EREADER, bytes(local_ereader), "System Bus"))

            # handle receiving items
            recv_amount = int.from_bytes(items_received, "little")
            if recv_amount < len(ctx.items_received):
                item: NetworkItem = ctx.items_received[recv_amount]
                item_id: int = item.item
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_names.lookup_in_game(item_id), 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

                writes.append((PINBALL_RECEIVED, int.to_bytes(recv_amount+1, 2, "little"), "System Bus"))
                # for the moment, just play a standard sfx for every item
                if item_id == 6:
                    writes.append(get_sfx_write(0xB2))
                else:
                    writes.append(get_sfx_write(0xD8))
                if item.location > 0:
                    self.message_queue.append((item_id, item.player))
                else:
                    # edge case, if it's from core we need to know the location instead of player
                    self.message_queue.append((item_id, item.location))
                if item_id & 0x200:
                    self.item_queue.append(item)

            if len(self.item_queue):
                item = self.item_queue.pop(0)
                idx = item.item & 0xF
                if idx == 0:
                    balls = int.from_bytes(current_balls, "little")
                    writes.append((PINBALL_LIVES, int.to_bytes(balls + 1, 1, "little"), "System Bus"))
                elif idx in (1, 2):
                    if idx == 1:
                        score = random.randint(1000000, 9000000)
                    else:
                        score = random.randint(100, 900)
                    # detranslate the score
                    writes.append((PINBALL_SCORE_ADD, score.to_bytes(4, "little"), "System Bus"))
                elif idx == 3:
                    writes.append((PINBALL_SAVER, int.to_bytes(1800, 2, "little"), "System Bus"))
            if "DeathLink" in ctx.tags:
                if self.pending_death_link:
                    writes.append((PINBALL_DEATHLINK_RECV, int.to_bytes(1, 1, "little"), "System Bus"))
                    self.pending_death_link = False

                if deathlink_send[0] and ctx.last_death_link + 1 < time.time():
                    writes.append((PINBALL_DEATHLINK_SEND, int.to_bytes(0, 1, "little"), "System Bus"))
                    await self.send_deathlink(ctx)

            # handle most items state based
            item: NetworkItem
            remote_boards = ((any(item.item == 2 for item in ctx.items_received) << 1)
                             + any(item.item == 1 for item in ctx.items_received))
            if boards[0] & remote_boards != remote_boards:
                writes.append((PINBALL_BOARDS, remote_boards.to_bytes(1, "little"), "System Bus"))

            # areas
            write_stages = bytearray(stages)
            writing_stages = False
            for area in range(14):
                if not stages[area] and any(item.item == 0x100 + area for item in ctx.items_received):
                    writing_stages = True
                    write_stages[area] = 1

            if writing_stages:
                writes.append((PINBALL_STAGES, bytes(write_stages), "System Bus"))

            remote_lives = sum(item.item == 3 for item in ctx.items_received)
            if starting_lives[0] != remote_lives:
                writes.append((PINBALL_STARTING_LIVES, remote_lives.to_bytes(1, "little"), "System Bus"))

            remote_coins = sum(item.item == 4 for item in ctx.items_received)
            remote_coins = min(remote_coins * 10, 99)
            if starting_coins[0] != remote_coins:
                writes.append((PINBALL_STARTING_COINS, remote_coins.to_bytes(1, "little"), "System Bus"))

            remote_ball = sum(item.item == 5 for item in ctx.items_received)
            if starting_ball[0] != remote_ball:
                writes.append((PINBALL_STARTING_BALL, remote_ball.to_bytes(1, "little"), "System Bus"))

            remote_pichu = any(item.item == 6 for item in ctx.items_received)
            if pichu_upgrade[0] != remote_pichu:
                writes.append((PINBALL_PICHU_UPGRADE, remote_pichu.to_bytes(1, "little"), "System Bus"))

            remote_get = int(any(item.item == 10 for item in ctx.items_received))
            if get_arrows[0] != remote_get:
                writes.append((PINBALL_GET, remote_get.to_bytes(1, "little"), "System Bus"))

            remote_evo = min((sum(item.item == 11 for item in ctx.items_received) +
                             (3 * sum(item.item == 12 for item in ctx.items_received))), 3)
            if evo_arrows[0] != remote_evo:
                writes.append((PINBALL_EVO, remote_evo.to_bytes(1, "little"), "System Bus"))

            for item in [item for item in ctx.items_received if item.item in range(13, 17)]:
                if local_dex[item.item - 13 + 201] < 3:
                    writing_dex = True
                    write_local_dex[item.item - 13 + 201] = 3

            remote_eggs = 0
            valid_eggs = False
            for item in [item for item in ctx.items_received if item.item in range(17, 24)]:
                egg_group = item.item - 17
                for mon in egg_groups[egg_group]:
                    remote_eggs |= (1 << mon)
                if egg_group < 5 or (egg_group == 5 and any(item.item == 1 for item in ctx.items_received)) or \
                    (egg_group == 6 and any(item.item == 2 for item in ctx.items_received)):
                    valid_eggs = True
            if remote_eggs and int.from_bytes(local_eggs, "little") != remote_eggs:
                writes.append((PINBALL_EGGS, remote_eggs.to_bytes(4, "little"), "System Bus"))
            if valid_eggs and int.from_bytes(hatch_mode, "little") != 1:
                writes.append((PINBALL_HATCH, int.to_bytes(1, 1, "little"), "System Bus"))

            remote_evo_items = 0
            for item in [item for item in ctx.items_received if item.item & 0x400 != 0]:
                remote_evo_items |= (1 << (item.item & 0xFF))
            if remote_evo_items and int.from_bytes(evo_items, "little") != remote_evo_items:
                writes.append((PINBALL_EVO_ITEMS, remote_evo_items.to_bytes(2, "little"), "System Bus"))

            # Helpers
            remote_helpers = 0
            for item in [item for item in ctx.items_received if item.item & 0x800 != 0]:
                remote_helpers |= (1 << (item.item & 0xFF))
            if remote_helpers and int.from_bytes(helpers, "little") != remote_helpers:
                writes.append((PINBALL_HELPERS, remote_helpers.to_bytes(1, "little"), "System Bus"))

            remote_coin_arrows = sum(item.item == 24 for item in ctx.items_received)
            if remote_coin_arrows and int.from_bytes(coin_arrows, "little") != remote_coin_arrows:
                writes.append((PINBALL_COIN, remote_coin_arrows.to_bytes(1, "little"), "System Bus"))

            remote_coin_mod = any(item.item == 25 for item in ctx.items_received)
            if remote_coin_mod and int.from_bytes(coin_mod, "little") != 1:
                writes.append((PINBALL_COIN_MODIFIER, int.to_bytes(1, 1, "little"), "System Bus"))

            remote_medals = sum(item.item == 26 for item in ctx.items_received)
            if remote_medals and int.from_bytes(medals, "little") != remote_medals:
                writes.append((PINBALL_MEDALS, remote_medals.to_bytes(1, "little"), "System Bus"))

            remote_open_shop = any(item.item == 27 for item in ctx.items_received)
            if remote_open_shop and int.from_bytes(open_shop, "little") != 1:
                writes.append((PINBALL_ALWAYS_OPEN_SHOP, int.to_bytes(1, 1, "little"), "System Bus"))

            # Check dexnav here
            if self.dexnav is not None:
                if self.dexnav == -1:
                    logger.warning("Unable to find a Pokémon by that name.")
                elif self.dexnav in special_encounters:
                    # check if we have the coins here
                    coin = int.from_bytes(coins, "little")
                    caught = sum(mon == 4 for mon in local_dex)
                    if coin < 60:
                        logger.warning("More coins are required to track this Pokémon.")
                    elif self.dexnav != 154 and caught < 100:
                        logger.warning("Cannot track special Pokémon until more Pokémon have been registered in the "
                                       "Pokédex!")
                    else:
                        writes.append((PINBALL_COINS, int.to_bytes(coin - 60, 1, "little"), "System Bus"))
                        if self.dexnav == 154:
                            address = PINBALL_FORCE_PICHU
                        else:
                            address = PINBALL_FORCE_SPECIAL
                        writes.append((address, int.to_bytes(1, 1, "little"), "System Bus"))
                        logger.warning(f"Attempting to track a special Pokémon!")
                        if "RingLink" in ctx.tags:
                            # process the RL event here
                            await ctx.send_msgs([
                                {
                                    "cmd": "Bounce",
                                    "tags": ["RingLink"],
                                    "data": {
                                        "amount": -60,
                                        "time": time.time(),
                                        "source": self.ringlink_id
                                    }
                                }
                            ])
                else:
                    writes.append((PINBALL_DEXNAV, int.to_bytes(self.dexnav + 1, 1, "little"), "System Bus"))
                    logger.warning(f"Attempting to track nearby {POKEDEX_INVERSE[self.dexnav]}!")
                self.dexnav = None

            if msg_mode[0] == 0 and self.message_queue:
                # only write if we aren't already
                item_id, player = self.message_queue.pop(0)
                writes.extend([
                    (PINBALL_STR_MODE, int.to_bytes(1, 1, "little"), "System Bus"),
                    (PINBALL_STR_ITEM, item_id.to_bytes(2, "little"), "System Bus"),
                    (PINBALL_STR_PLAYER, player.to_bytes(4, "little", signed=True), "System Bus"),
                ])

            # check ringlink here
            if "RingLink" in ctx.tags:
                coin_total = int.from_bytes(coin_plus, "little") - int.from_bytes(coin_minus, "little")
                if coin_total:  # just need non-zero
                    await ctx.send_msgs([
                        {
                            "cmd": "Bounce",
                            "tags": ["RingLink"],
                            "data": {
                                "amount": coin_total,
                                "time": time.time(),
                                "source": self.ringlink_id
                            }
                        }
                    ])
                    writes.extend([
                        (PINBALL_RINGLINK_PACKET_GAIN, int.to_bytes(0, 1, "little"), "System Bus"),
                        (PINBALL_RINGLINK_PACKET_LOSS, int.to_bytes(0, 1, "little"), "System Bus"),
                    ])

                if self.ringlink_incoming and not self.dexnav:
                    # dexnav will cause some timing issues, we'll defer to it first and then fixup ringlink next iteration
                    if self.ringlink_incoming > 0:
                        # just use the ingame functions
                        writes.extend(get_coin_give_write(self.ringlink_incoming))
                    else:
                        # gotta do it manually
                        coin = int.from_bytes(coins, "little")
                        writes.append((PINBALL_COINS, int.to_bytes(max(0, coin + self.ringlink_incoming),
                                                                   1, "little"), "System Bus"))
                    self.ringlink_incoming = 0

            new_checks = []
            # check for locations

            for i in range(205):
                if local_dex[i] == 4 and (i+1) not in ctx.locations_checked:
                    new_checks.append(i+1)
                elif (slot_info[0] & 0x1) and local_dex[i] != 4 and (i+1) in ctx.checked_locations:
                    # collect
                    writing_dex = True
                    write_local_dex[i] = 4

            for i in range(8):
                mask = 1 << i
                if bonus_stages[0] & mask and (0x100 + i) not in ctx.locations_checked:
                    new_checks.append(0x100 + i)

            ruby_bumper_hits = int.from_bytes(ruby_bumper, "little")
            sapphire_bumper_hits = int.from_bytes(sapphire_bumper, "little")
            ruby_ball_upgrade_hits = int.from_bytes(ruby_ball_upgrade, "little")
            sapphire_ball_upgrade_hits = int.from_bytes(sapphire_ball_upgrade, "little")
            maku_ball_upgrade_hits = int.from_bytes(maku_ball_upgrade, "little")

            ruby_bumper_locs = [loc for loc in ctx.missing_locations if loc & 0xF00 == 0x200 and loc & 0xFF < 100]
            sapphire_bumper_locs = [loc for loc in ctx.missing_locations if loc & 0xF00 == 0x200 and loc & 0xFF >= 100]
            ruby_upgrade_locs = [loc for loc in ctx.missing_locations if loc & 0xF00 == 0x300 and loc & 0xFF < 100]
            sapphire_upgrade_locs = [loc for loc in ctx.missing_locations if loc & 0xF00 == 0x300 and loc & 0xFF >= 100]
            maku_upgrade_locs = [loc for loc in ctx.missing_locations if loc & 0xF00 == 0x400]

            for loc in ruby_bumper_locs:
                idx = loc & 0xFF
                if idx <= ruby_bumper_hits:
                    new_checks.append(loc)

            for loc in sapphire_bumper_locs:
                idx = (loc & 0xFF) - 100
                if idx <= sapphire_bumper_hits:
                    new_checks.append(loc)

            for loc in ruby_upgrade_locs:
                idx = loc & 0xFF
                if idx <= ruby_ball_upgrade_hits:
                    new_checks.append(loc)

            for loc in sapphire_upgrade_locs:
                idx = (loc & 0xFF) - 100
                if idx <= sapphire_ball_upgrade_hits:
                    new_checks.append(loc)

            for loc in maku_upgrade_locs:
                idx = loc & 0xFF
                if idx <= maku_ball_upgrade_hits:
                    new_checks.append(loc)

            # collect behaviors here
            if ruby_bumper_locs:
                min_ruby_bumper = min(ruby_bumper_locs) & 0xFF
            else:
                min_ruby_bumper = 0
            if sapphire_bumper_locs:
                min_sapphire_bumper = (min(sapphire_bumper_locs) & 0xFF) - 100
            else:
                min_sapphire_bumper = 0
            if ruby_upgrade_locs:
                min_ruby_upgrade = min(ruby_upgrade_locs) & 0xFF
            else:
                min_ruby_upgrade = 0
            if sapphire_upgrade_locs:
                min_sapphire_upgrade = (min(sapphire_upgrade_locs) & 0xFF) - 100
            else:
                min_sapphire_upgrade = 0
            if maku_upgrade_locs:
                min_maku_upgrade = min(maku_upgrade_locs) & 0xFF
            else:
                min_maku_upgrade = 0

            if ruby_bumper_hits < min_ruby_bumper - 1:
                writes.append((PINBALL_RUBY_BUMPER, int.to_bytes(min_ruby_bumper - 1, 1, "little"), "System Bus"))
            if sapphire_bumper_hits < min_sapphire_bumper - 1:
                writes.append((PINBALL_SAPPHIRE_BUMPER, int.to_bytes(min_sapphire_bumper - 1, 1, "little"), "System Bus"))
            if ruby_ball_upgrade_hits < min_ruby_upgrade - 1:
                writes.append((PINBALL_RUBY_BALL_UPGRADE, int.to_bytes(min_ruby_upgrade - 1, 1, "little"), "System Bus"))
            if sapphire_ball_upgrade_hits < min_sapphire_upgrade - 1:
                writes.append((PINBALL_SAPPHIRE_BALL_UPGRADE, int.to_bytes(min_sapphire_upgrade - 1, 1, "little"), "System Bus"))
            if maku_ball_upgrade_hits < min_maku_upgrade - 1:
                writes.append((PINBALL_MAKUHITA_BALL_UPGRADE, int.to_bytes(min_maku_upgrade - 1, 1, "little"), "System Bus"))

            shop_collect: dict[int, int] = {}

            for i in range(2):
                for j in range(int.from_bytes(shop_tracks) + 1):
                    for k in range(1, int.from_bytes(shop_len) + 1):
                        idx = 0x500 + (i * 75) + (j * 15) + k
                        if shops[i*5 + j] >= k:
                            if idx not in ctx.checked_locations:
                                new_checks.append(idx)
                        else:
                            if idx in ctx.checked_locations:
                                shop_collect[i*5 + j] = k
                            else:
                                break

            roulette_collect: dict[int, int] = {}

            for i in range(2):
                for j in range(1, int.from_bytes(roulette_len) + 1):
                    idx = 0x600 + (i * 40) + j
                    if roulettes[i] >= j:
                        if idx not in ctx.checked_locations:
                            new_checks.append(idx)
                    else:
                        if idx in ctx.checked_locations:
                            roulette_collect[i] = j
                        else:
                            break

            for ptr, val in shop_collect.items():
                writes.append((PINBALL_SHOPS + ptr, int.to_bytes(val, 1, "little"), "System Bus"))

            for ptr, val in roulette_collect.items():
                writes.append((PINBALL_ROULETTES + ptr, int.to_bytes(val, 1, "little"), "System Bus"))

            # handle remote dex here
            if self.pokedex_key in ctx.stored_data:
                compressed = compress_pokedex(write_local_dex)
                if list(compressed.to_bytes(26, "little")) != ctx.stored_data[self.pokedex_key]:
                    writing_dex = True
                    compressed |= int.from_bytes(ctx.stored_data[self.pokedex_key], "little")
                    decompressed = decompress_pokedex(compressed)
                    for i in range(len(decompressed)):
                        if decompressed[i] == 4 and write_local_dex[i] != 4:
                            write_local_dex[i] = 4
                    await ctx.send_msgs([
                        {
                            "cmd": "Set", "key": self.pokedex_key, "operations": [
                                {"operation": "replace", "value": list(compressed.to_bytes(26, "little"))}
                            ]
                        }
                    ])

            if writing_dex:
                await guarded_write(ctx.bizhawk_ctx, [(PINBALL_POKEDEX, bytes(write_local_dex), "System Bus")],
                                    [(PINBALL_POKEDEX, local_dex, "System Bus")])

            await write(ctx.bizhawk_ctx, writes)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                location = ctx.location_names.lookup_in_game(new_check_id)
                gba_logger.info(
                    f'New Check: {location} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
        except Exception as ex:
            from traceback import print_exc
            Utils.messagebox("Error", str(ex))
            print_exc()
