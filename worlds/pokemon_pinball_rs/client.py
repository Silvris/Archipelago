import logging
import time
from enum import IntEnum
from base64 import b64encode
from typing import TYPE_CHECKING, Any
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient
from MultiServer import mark_raw

from .data.pokemon import egg_groups

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

gba_logger = logging.getLogger("GBA")
logger = logging.getLogger("Client")

PINBALL_MAIN = 0x200B0C0
PINBALL_EREADER = PINBALL_MAIN + 0x7  # size 0x05
PINBALL_POKEDEX = PINBALL_MAIN + 0x74  # Size 0xCD
PINBALL_HIGH_SCORES = PINBALL_MAIN + 0x158  # Size 0x17F


PINBALL_CURRENT = 0x2000000  # It can technically be different, but in reality it never is

PINBALL_AP_START = 0x2033000
PINBALL_STARTING_LIVES = PINBALL_AP_START
PINBALL_STARTING_COINS = PINBALL_AP_START + 1
PINBALL_STARTING_BALL = PINBALL_AP_START + 2
PINBALL_PICHU_UPGRADE = PINBALL_AP_START + 3
# PINBALL_COIN_MODIFIER = PINBALL_AP_START + 4
PINBALL_BOARDS = PINBALL_AP_START + 5
PINBALL_SFX = PINBALL_AP_START + 6
PINBALL_GET = PINBALL_AP_START + 8
PINBALL_EVO = PINBALL_AP_START + 9
PINBALL_HATCH = PINBALL_AP_START + 10
PINBALL_RECEIVED = PINBALL_AP_START + 11
PINBALL_STAGES = PINBALL_AP_START + 0x10
PINBALL_EGGS = PINBALL_AP_START + 0x20

PINBALL_NAME = 0x6BC000
PINBALL_VERSION = 0x6BC020
PINBALL_GOAL = 0x6BC030
PINBALL_DEX_REQ = 0x6BC031
PINBALL_SCORE_REQ = 0x6BC032
PINBALL_TARGET_REQ = 0x6BC03A


EREADER_MAP: dict[str, tuple[int, int]] = {
    "Special Guests": (0, 7),
    "Encounter Rate Up": (1, 8),
    "Ruins Area": (3, 9),
}

@mark_raw
def cmd_ereader(self: "BizHawkClientCommandProcessor", card: str) -> None:
    """Check the current pool of EnergyLink, and requestable refills from it."""
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

    if card not in EREADER_MAP:
        logger.warning(f"{card} is not a valid E-Reader card.")
        return
    if not client.has_item(self.ctx, EREADER_MAP[card][1]):
        logger.warning(f"You have not received the {card} E-Reader card.")
    client.active_ereader = EREADER_MAP[card][0]

def get_sfx_write(sfx: int) -> tuple[int, bytes, str]:
    return PINBALL_SFX, sfx.to_bytes(2, 'big'), "System Bus"


class PinballRSClient(BizHawkClient):
    game = "Pokemon Pinball Ruby & Sapphire"
    system = "GBA"
    patch_suffix = ".appbrs"
    item_queue: list[NetworkItem] = []
    rom: bytes | None = None
    active_ereader: int = -1

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read, get_memory_size
        from . import PokemonPinballRSWorld

        try:
            if (await get_memory_size(ctx.bizhawk_ctx, "ROM")) < 0x700000:
                if "ereader" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("ereader")
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

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict[str, Any]) -> None:
        pass  # TODO: RingLink

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death(f"{ctx.player_names[ctx.slot]} is bad at pinball.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    @staticmethod
    def has_item(ctx: "BizHawkClientContext", idx: int):
        return any(item.item == idx for item in ctx.items_received)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write

        if ctx.server is None:
            return

        if ctx.slot is None:
            return

        # get our relevant bytes
        (local_dex, high_scores, starting_lives, starting_coins, starting_ball, pichu_upgrade,
            boards, get_arrows, evo_arrows, hatch_mode, stages, items_received, local_eggs, e_reader,
         goal, dex_req, score_req, target_req) = await read(ctx.bizhawk_ctx, [
                (PINBALL_POKEDEX, 205, "System Bus"),
                (PINBALL_HIGH_SCORES, 0x180, "System Bus"),
                (PINBALL_STARTING_LIVES, 1, "System Bus"),
                (PINBALL_STARTING_COINS, 1, "System Bus"),
                (PINBALL_STARTING_BALL, 1, "System Bus"),
                (PINBALL_PICHU_UPGRADE, 1, "System Bus"),
                (PINBALL_BOARDS, 1, "System Bus"),
                (PINBALL_GET, 1, "System Bus"),
                (PINBALL_EVO, 1, "System Bus"),
                (PINBALL_HATCH, 1, "System Bus"),
                (PINBALL_STAGES, 14, "System Bus"),
                (PINBALL_RECEIVED, 2, "System Bus"),
                (PINBALL_EGGS, 4, "System Bus"),
                (PINBALL_EREADER, 5, "System Bus"),
                (PINBALL_GOAL, 1, "ROM"),
                (PINBALL_DEX_REQ, 1, "ROM"),
                (PINBALL_SCORE_REQ, 8, "ROM"),
                (PINBALL_TARGET_REQ, 26, "ROM"),
            ])

        goal_is_cleared = True

        if goal[0] & 1 and goal_is_cleared:
            caught = sum(mon == 4 for mon in local_dex)
            if caught < int.from_bytes(dex_req, "big"):
                goal_is_cleared = False

        if goal[0] & 2 and goal_is_cleared:
            # scores are kind of a pain, it's 16 bytes for **4** character names, then 8 byte score
            for i in range(0, len(high_scores), 24):
                score_lo = int.from_bytes(high_scores[i+20:], "big")
                score_hi = int.from_bytes(high_scores[i+16:i+20], "big")
                # score_lo is capped at 99,999,999. We should be below that, but cap it if we are above
                score = min(score_lo, 99999999) + (score_hi * 100000000)
                if score > int.from_bytes(score_req, "big"):
                    break
            else:
                goal_is_cleared = False

        if goal[0] & 4 and goal_is_cleared:
            # pretty easy, just run through all 205
            for i in range(205):
                idx = i // 8
                mask = i % 8
                if target_req[idx] & (1 << mask):
                    if not local_dex[i] == 4:
                        goal_is_cleared = False

        if not ctx.finished_game and goal_is_cleared:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
        writes = []

        write_local_dex = bytearray(local_dex)
        writing_dex = False

        local_ereader = bytearray(e_reader)
        if self.active_ereader:
            local_ereader[self.active_ereader] = 1

        if bytes(local_ereader) != e_reader:
            writes.append((PINBALL_EREADER, bytes(local_ereader), "System Bus"))

        # handle receiving items
        recv_amount = int.from_bytes(items_received, "big")
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

            writes.append((PINBALL_RECEIVED, int.to_bytes(recv_amount+1, 2, "big"), "System Bus"))
            # for the moment, just play a standard sfx for every item
            if item.item == 4:
                writes.append(get_sfx_write(0xB2))
            else:
                writes.append(get_sfx_write(0xD8))

        if len(self.item_queue):
            item = self.item_queue.pop(0)
            idx = item.item & 0xF

        # handle most items state based
        item: NetworkItem
        remote_boards = ((any(item.item == 2 for item in ctx.items_received) << 1)
                         + any(item.item == 1 for item in ctx.items_received))
        if boards[0] & remote_boards != remote_boards:
            writes.append((PINBALL_BOARDS, remote_boards.to_bytes(1, "big"), "System Bus"))

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
            writes.append((PINBALL_STARTING_LIVES, remote_lives.to_bytes(1, "big"), "System Bus"))

        remote_coins = sum(item.item == 4 for item in ctx.items_received)
        if starting_coins[0] != remote_coins:
            writes.append((PINBALL_STARTING_COINS, remote_coins.to_bytes(1, "big"), "System Bus"))

        remote_ball = sum(item.item == 5 for item in ctx.items_received)
        if starting_ball[0] != remote_ball:
            writes.append((PINBALL_STARTING_BALL, remote_ball.to_bytes(1, "big"), "System Bus"))

        remote_get = int(any(item.item == 10 for item in ctx.items_received))
        if get_arrows[0] != remote_get:
            writes.append((PINBALL_GET, remote_get.to_bytes(1, "big"), "System Bus"))

        remote_evo = sum(item.item == 11 for item in ctx.items_received)
        if evo_arrows[0] != remote_evo:
            writes.append((PINBALL_EVO, remote_evo.to_bytes(1, "big"), "System Bus"))

        for item in [item for item in ctx.items_received if item.item in range(13, 17)]:
            if local_dex[item.item - 13 + 200] < 3:
                writing_dex = True
                write_local_dex[item.item - 13 + 200] = 3

        remote_eggs = 0
        for item in [item for item in ctx.items_received if item.item in range(17, 23)]:
            egg_group = item.item - 16
            for mon in egg_groups[egg_group]:
                remote_eggs |= (1 << mon)
        if remote_eggs and int.from_bytes(local_eggs, "little") != remote_eggs:
            writes.append((PINBALL_EGGS, remote_eggs.to_bytes(4, "big"), "System Bus"))
            writes.append((PINBALL_HATCH, int.to_bytes(1, 1, "big"), "System Bus"))

        new_checks = []
        # check for locations

        for i in range(205):
            if local_dex[i] == 4 and (i+1) not in ctx.locations_checked:
                new_checks.append(i+1)
            # elif local_dex[i] != 4 and (i+1) in ctx.checked_locations:
            #    # collect, maybe push out to an option?
            #    writing_dex = True
            #    write_local_dex[i] = 4

        if writing_dex:
            writes.append((PINBALL_POKEDEX, bytes(write_local_dex), "System Bus"))

        await write(ctx.bizhawk_ctx, writes)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            gba_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
