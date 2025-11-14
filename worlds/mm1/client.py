import logging
import time
from enum import IntEnum
from base64 import b64encode
from typing import TYPE_CHECKING, Dict, Tuple, List, Optional, Any
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

nes_logger = logging.getLogger("NES")
logger = logging.getLogger("Client")


class MM1EnergyLinkType(IntEnum):
    Life = 0
    RollingCutter = 1
    IceSlasher = 2
    HyperBomb = 3
    FireStorm = 4
    ThunderBeam = 5
    SuperArm = 6
    MagnetBeam = 7
    OneUP = 8


request_to_name: Dict[str, str] = {
    "HP": "health",
    "RC": "Rolling Cutter energy",
    "IS": "Ice Slasher energy",
    "HB": "Hyper Bomb energy",
    "FS": "Fire Storm energy",
    "TB": "Thunder Beam energy",
    "SA": "Super Arm energy",
    "MB": "Magnet Beam energy",
    "1U": "lives"
}

HP_EXCHANGE_RATE = 500000000
WEAPON_EXCHANGE_RATE = 250000000
ONEUP_EXCHANGE_RATE = 14000000000

MM1_UNLOCKED_WEAPONS = 0x5D
MM1_HEALTH = 0x6A  # weapon energy immediately follows
MM1_LIVES = 0xA6
MM1_RECEIVED_ITEMS = 0xC0
MM1_CLEARED_RBM = 0xC1
MM1_UNLOCKED_RBM = 0xC2
MM1_DEATHLINK = 0xC3
MM1_ENERGYLINK_PACKET = 0xC4
MM1_MAGNET_BEAM = 0xC5
MM1_LAST_WILY = 0xC6
MM1_COMPLETED_STAGES = 0xC7  # and C8
MM1_SFX_QUEUE = 0xC9
MM1_RBM_STROBE = 0xCA  # not implemented yet
MM1_BOSS_REFIGHTS = 0xCB

MM1_STAGE_CHECKS = {
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 0xA,
    8: 0xB,
}

MM1_REFIGHTS = {
    0: 8,
    1: 0xE,
    2: 0xC,
    3: 0xD,
    4: 0x9,
    5: 0xF
}

MM1_RBM_REMAP = {
    1: 0x20,
    2: 0x10,
    3: 0x2,
    4: 0x40,
    5: 0x4,
    6: 0x8,
}

def cmd_pool(self: "BizHawkClientCommandProcessor") -> None:
    """Check the current pool of EnergyLink, and requestable refills from it."""
    if self.ctx.game != "Mega Man":
        logger.warning("This command can only be used when playing Mega Man.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    energylink = self.ctx.stored_data.get(f"EnergyLink{self.ctx.team}", 0)
    health_points = energylink // HP_EXCHANGE_RATE
    weapon_points = energylink // WEAPON_EXCHANGE_RATE
    lives = energylink // ONEUP_EXCHANGE_RATE
    logger.info(f"Healing available: {health_points}\n"
                f"Weapon refill available: {weapon_points}\n"
                f"Lives available: {lives}")


def cmd_request(self: "BizHawkClientCommandProcessor", amount: str, target: str) -> None:
    from worlds._bizhawk.context import BizHawkClientContext
    """Request a refill from EnergyLink."""
    if self.ctx.game != "Mega Man":
        logger.warning("This command can only be used when playing Mega Man.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    valid_targets: Dict[str, MM1EnergyLinkType] = {
        "HP": MM1EnergyLinkType.Life,
        "RC": MM1EnergyLinkType.RollingCutter,
        "IS": MM1EnergyLinkType.IceSlasher,
        "HB": MM1EnergyLinkType.HyperBomb,
        "FS": MM1EnergyLinkType.FireStorm,
        "TB": MM1EnergyLinkType.ThunderBeam,
        "SA": MM1EnergyLinkType.SuperArm,
        "MB": MM1EnergyLinkType.MagnetBeam,
        "1U": MM1EnergyLinkType.OneUP
    }
    if target.upper() not in valid_targets:
        logger.warning(f"Unrecognized target {target.upper()}. Available targets: {', '.join(valid_targets.keys())}")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, MegaMan1Client)
    client.refill_queue.append((valid_targets[target.upper()], int(amount)))
    logger.info(f"Restoring {amount} {request_to_name[target.upper()]}.")


def cmd_autoheal(self) -> None:
    """Enable auto heal from EnergyLink."""
    if self.ctx.game != "Mega Man":
        logger.warning("This command can only be used when playing Mega Man.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    else:
        assert isinstance(self.ctx.client_handler, MegaMan1Client)
        if self.ctx.client_handler.auto_heal:
            self.ctx.client_handler.auto_heal = False
            logger.info(f"Auto healing disabled.")
        else:
            self.ctx.client_handler.auto_heal = True
            logger.info(f"Auto healing enabled.")


def get_sfx_writes(sfx: int) -> Tuple[Tuple[int, bytes, str], ...]:
    return (MM1_SFX_QUEUE, sfx.to_bytes(1, 'little'), "RAM"),


class MegaMan1Client(BizHawkClient):
    game = "Mega Man"
    system = "NES"
    patch_suffix = ".apmm1"
    item_queue: List[NetworkItem] = []
    pending_death_link: bool = False
    # default to true, as we don't want to send a deathlink until Mega Man's HP is initialized once
    sending_death_link: bool = True
    death_link: bool = False
    energy_link: bool = False
    rom: bytes | None = None
    weapon_energy: int = 0
    health_energy: int = 0
    auto_heal: bool = False
    refill_queue: List[Tuple[MM1EnergyLinkType, int]] = []
    last_wily: Optional[int] = None  # default to wily 1

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read, get_memory_size
        from . import MM1World

        try:
            if (await get_memory_size(ctx.bizhawk_ctx, "PRG ROM")) < 0x1FFFF:
                if "pool" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("pool")
                if "request" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("request")
                if "autoheal" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("autoheal")
                return False

            game_name, version = (await read(ctx.bizhawk_ctx, [(0x1FFE0, 16, "PRG ROM"),
                                                               (0x1FFDD, 3, "PRG ROM")]))
            if game_name[:3] != b"MM1" or version != bytes(MM1World.world_version):
                if game_name[:3] == b"MM1":
                    # I think this is an easier check than the other?
                    older_version = "unknown" if version == b"\xFF\xFF\xFF" else f"{version[0]}.{version[1]}.{version[2]}"
                    logger.warning(f"This Mega Man patch was generated for an different version of the apworld. "
                                   f"Please use that version to connect instead.\n"
                                   f"Patch version: ({older_version})\n"
                                   f"Client version: ({'.'.join([str(i) for i in MM1World.world_version])})")
                if "pool" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("pool")
                if "request" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("request")
                if "autoheal" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("autoheal")
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        self.rom = game_name
        ctx.items_handling = 0b111
        ctx.want_slot_data = False
        deathlink = (await read(ctx.bizhawk_ctx, [(0x1FFDC, 1, "PRG ROM")]))[0][0]
        if deathlink & 0x01:
            self.death_link = True
        if deathlink & 0x02:
            self.energy_link = True

        if self.energy_link:
            if "pool" not in ctx.command_processor.commands:
                ctx.command_processor.commands["pool"] = cmd_pool
            if "request" not in ctx.command_processor.commands:
                ctx.command_processor.commands["request"] = cmd_request
            if "autoheal" not in ctx.command_processor.commands:
                ctx.command_processor.commands["autoheal"] = cmd_autoheal

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)
        elif cmd == "Retrieved":
            if f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.last_wily = args["keys"][f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}"]
        elif cmd == "Connected":
            if self.energy_link:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death("Mega Man was defeated.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write

        if ctx.server is None:
            return

        if ctx.slot is None:
            return

        # get our relevant bytes
        items_received, robot_masters_unlocked, robot_masters_defeated, magnet_beam_get, \
            weapons_unlocked, lives, weapon_energy, health, death_link_status, \
            energy_link_packet, last_wily, completed_stages, boss_refights = await read(ctx.bizhawk_ctx, [
                (MM1_RECEIVED_ITEMS, 1, "RAM"),
                (MM1_UNLOCKED_RBM, 1, "RAM"),
                (MM1_CLEARED_RBM, 1, "RAM"),
                (MM1_MAGNET_BEAM, 1, "RAM"),
                (MM1_UNLOCKED_WEAPONS, 1, "RAM"),
                (MM1_LIVES, 1, "RAM"),
                (MM1_HEALTH+1, 7, "RAM"),
                (MM1_HEALTH, 1, "RAM"),
                (MM1_DEATHLINK, 1, "RAM"),
                (MM1_ENERGYLINK_PACKET, 1, "RAM"),
                (MM1_LAST_WILY, 1, "RAM"),
                (MM1_COMPLETED_STAGES, 2, "RAM"),
                (MM1_BOSS_REFIGHTS, 1, "RAM"),
            ])

        #if difficulty[0] not in (0, 1):
        #    return  # Game is not initialized

        if not ctx.finished_game and (completed_stages[1] & 0x2) != 0:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
        writes = []

        # deathlink
        if self.death_link:
            await ctx.update_death_link(self.death_link)
        if self.pending_death_link:
            writes.append((MM1_DEATHLINK, bytes([0x01]), "RAM"))
            self.pending_death_link = False
            self.sending_death_link = True
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            if health[0] == 0x00 and not self.sending_death_link:
                await self.send_deathlink(ctx)
            elif health[0] != 0x00 and not death_link_status[0]:
                self.sending_death_link = False

        if self.last_wily != last_wily[0]:
            if self.last_wily is None:
                # revalidate last wily from data storage
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM1_LAST_WILY_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "default", "value": 8}
                ]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [f"MM1_LAST_WILY_{ctx.team}_{ctx.slot}"]}])
            elif last_wily[0] == 0:
                writes.append((MM1_LAST_WILY, self.last_wily.to_bytes(1, "little"), "RAM"))
            else:
                # correct our setting
                self.last_wily = last_wily[0]
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "replace", "value": self.last_wily}
                ]}])

        # handle receiving items
        recv_amount = items_received[0]
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

            if item.item & 0x30 == 0:
                # Robot Master Weapon
                new_weapons = weapons_unlocked[0] | (1 << ((item.item & 0xF) - 1))
                writes.append((MM1_UNLOCKED_WEAPONS, new_weapons.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x22))
            elif item.item & 0x20 == 0:
                # Robot Master Stage Access
                new_stages = robot_masters_unlocked[0] | MM1_RBM_REMAP[item.item & 0xF]
                writes.append((MM1_UNLOCKED_RBM, new_stages.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x1C))
                writes.append((MM1_RBM_STROBE, b"\x01", "RAM"))
            else:
                # append to the queue, so we handle it later
                self.item_queue.append(item)
            recv_amount += 1
            writes.append((MM1_RECEIVED_ITEMS, recv_amount.to_bytes(1, 'little'), "RAM"))

        if energy_link_packet[0]:
            pickup = energy_link_packet[0]
            if pickup in (0x02, 0x06):
                # Health pickups
                value = pickup
                exchange_rate = HP_EXCHANGE_RATE
            elif pickup in (0x82, 0x86):
                # Weapon Energy
                value = (pickup & 0xF)
                exchange_rate = WEAPON_EXCHANGE_RATE
            elif pickup == 0xFE:
                # 1-Up
                value = 1
                exchange_rate = ONEUP_EXCHANGE_RATE
            else:
                # if we managed to pickup something else, we should just fall through
                value = 0
                exchange_rate = 0
            contribution = (value * exchange_rate) >> 1
            if contribution:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                        [{"operation": "add", "value": contribution},
                         {"operation": "max", "value": 0}]}])
            logger.info(f"Deposited {contribution / HP_EXCHANGE_RATE} health into the pool.")
            writes.append((MM1_ENERGYLINK_PACKET, 0x00.to_bytes(1, "little"), "RAM"))

        if self.weapon_energy:
            # Weapon Energy
            # We parse the whole thing to spread it as thin as possible
            current_energy = self.weapon_energy
            weapon_energy = bytearray(weapon_energy)
            for i, weapon in zip(range(len(weapon_energy)), weapon_energy):
                if weapon < 0x1C:
                    missing = 0x1C - weapon
                    if missing > self.weapon_energy:
                        missing = self.weapon_energy
                    self.weapon_energy -= missing
                    weapon_energy[i] = weapon + missing
                    if not self.weapon_energy:
                        writes.append((MM1_HEALTH + 1, weapon_energy, "RAM"))
                        break
            else:
                if current_energy != self.weapon_energy:
                    writes.append((MM1_HEALTH + 1, weapon_energy, "RAM"))

        if self.health_energy or self.auto_heal:
            # Health Energy
            # We save this if the player has not taken any damage
            current_health = health[0]
            if 0 < current_health < 0x1C:
                health_diff = 0x1C - current_health
                if self.health_energy:
                    if health_diff > self.health_energy:
                        health_diff = self.health_energy
                    self.health_energy -= health_diff
                else:
                    pool = ctx.stored_data.get(f"EnergyLink{ctx.team}", 0)
                    if health_diff * HP_EXCHANGE_RATE > pool:
                        health_diff = int(pool // HP_EXCHANGE_RATE)
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                            [{"operation": "add", "value": -health_diff * HP_EXCHANGE_RATE},
                             {"operation": "max", "value": 0}]}])
                current_health += health_diff
                writes.append((MM1_HEALTH, current_health.to_bytes(1, 'little'), "RAM"))

        if self.refill_queue:
            refill_type, refill_amount = self.refill_queue.pop()
            if refill_type == MM1EnergyLinkType.Life:
                exchange_rate = HP_EXCHANGE_RATE
            elif refill_type == MM1EnergyLinkType.OneUP:
                exchange_rate = ONEUP_EXCHANGE_RATE
            else:
                exchange_rate = WEAPON_EXCHANGE_RATE
            pool = ctx.stored_data.get(f"EnergyLink{ctx.team}", 0)
            request = exchange_rate * refill_amount
            if request > pool:
                logger.warning(
                    f"Not enough energy to fulfill the request. Maximum request: {pool // exchange_rate}")
            else:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                        [{"operation": "add", "value": -request},
                         {"operation": "max", "value": 0}]}])
                if refill_type == MM1EnergyLinkType.Life:
                    refill_ptr = MM1_HEALTH
                elif refill_type == MM1EnergyLinkType.OneUP:
                    refill_ptr = MM1_LIVES
                else:
                    refill_ptr = MM1_HEALTH + refill_type
                current_value = (await read(ctx.bizhawk_ctx, [(refill_ptr, 1, "RAM")]))[0][0]
                new_value = min(0x1C if refill_type != MM1EnergyLinkType.OneUP else 99, current_value + refill_amount)
                writes.append((refill_ptr, new_value.to_bytes(1, "little"), "RAM"))

        if len(self.item_queue):
            item = self.item_queue.pop(0)
            idx = item.item & 0xF
            if idx == 0:
                # 1-Up
                current_lives = lives[0]
                if current_lives > 99:
                    self.item_queue.append(item)
                else:
                    current_lives += 1
                    writes.append((MM1_LIVES, current_lives.to_bytes(1, 'little'), "RAM"))
                    writes.extend(get_sfx_writes(0x32))
            elif idx == 1:
                self.weapon_energy += 0xE
                writes.extend(get_sfx_writes(0x1a))
            elif idx == 2:
                self.health_energy += 0xE
                writes.extend(get_sfx_writes(0x1a))
            elif idx == 3:
                # Yashichi, full health and weapon refill
                writes.extend(get_sfx_writes(0x1a))
                writes.extend((MM1_HEALTH, bytes([0x1C]*8), "RAM"))

        await write(ctx.bizhawk_ctx, writes)

        new_checks = []
        # check for locations
        for i in range(1, 7):
            flag = 1 << (i - 1)
            if robot_masters_defeated[0] & MM1_RBM_REMAP[i]:
                wep_id = 0x10 + i
                if wep_id not in ctx.checked_locations:
                    new_checks.append(wep_id)
            if boss_refights[0] & flag:
                boss_id = MM1_REFIGHTS[i-1]
                if boss_id not in ctx.checked_locations:
                    new_checks.append(boss_id)

        if magnet_beam_get[0] & 0x80:
            new_checks.append(0x17)

        stages_complete = int.from_bytes(completed_stages, "little")
        for boss, boss_id in MM1_STAGE_CHECKS.items():
            if stages_complete & (1 << boss) != 0:
                if boss_id not in ctx.checked_locations:
                    new_checks.append(boss_id)

        #for consumable in MM2_CONSUMABLE_TABLE:
        #    if consumable not in ctx.checked_locations:
        #        is_checked = consumable_checks[MM2_CONSUMABLE_TABLE[consumable][0]] \
        #                     & MM2_CONSUMABLE_TABLE[consumable][1]
        #        if is_checked:
        #            new_checks.append(consumable)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            nes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
        await ctx.check_locations(new_checks)
