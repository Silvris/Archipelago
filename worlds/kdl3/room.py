import struct
from random import Random
from typing import Optional, Dict, TYPE_CHECKING, List, Union, Tuple
from BaseClasses import Region, ItemClassification, MultiWorld, Entrance
from worlds.Files import APTokenTypes
from .client_addrs import consumable_addrs, star_addrs

if TYPE_CHECKING:
    from entrance_rando import ERPlacementState
    from .rom import KDL3ProcedurePatch
    from . import KDL3World

animal_map = {
    "Rick Spawn": 0,
    "Kine Spawn": 1,
    "Coo Spawn": 2,
    "Nago Spawn": 3,
    "ChuChu Spawn": 4,
    "Pitch Spawn": 5
}

final_iceberg_rooms = {
    "Iceberg 6 - 8": "Spark Ability",
    "Iceberg 6 - 10": "Stone Ability",
    "Iceberg 6 - 12": "Parasol Ability",
    "Iceberg 6 - 14": "Ice Ability",
    "Iceberg 6 - 16": "Cutter Ability",
    "Iceberg 6 - 18": "Clean Ability",
    "Iceberg 6 - 20": "Burning Ability",
    "Iceberg 6 - 22": "Needle Ability",
}


class KDL3Door(Entrance):
    world: Optional["KDL3World"] = None
    parent_region: "KDL3Room"
    connected_region: "KDL3Room"


class KDL3Room(Region):
    entrance_type = KDL3Door
    pointer: int = 0
    level: int = 0
    stage: int = 0
    room: int = 0
    music: int = 0
    default_exits: Dict[str, Dict[str, Union[int, str, List[str]]]]
    animal_pointers: List[int]
    enemies: List[str]
    entity_load: List[List[int]]
    consumables: List[Dict[str, Union[int, str]]]
    entrance_coords: List[List[int]]
    spawn: List[int]
    entrance_pointer: int
    default_spawn: bool

    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: Optional[str], level: int,
                 stage: int, room: int, pointer: int, music: int,
                 default_exits: Dict[str, Dict[str, Union[int, str, List[str]]]],
                 animal_pointers: List[int], enemies: List[str],
                 entity_load: List[List[int]],
                 consumables: List[Dict[str, Union[int, str]]], consumable_pointer: int,
                 entrances: List[List[int]], spawn: List[int], entrance_pointer: int,
                 index: int) -> None:
        super().__init__(name, player, multiworld, hint)
        self.level = level
        self.stage = stage
        self.room = room
        self.pointer = pointer
        self.music = music
        self.default_exits = default_exits
        self.animal_pointers = animal_pointers
        self.enemies = enemies
        self.entity_load = entity_load
        self.consumables = consumables
        self.consumable_pointer = consumable_pointer
        self.entrance_coords = entrances
        self.spawn = spawn
        self.entrance_pointer = entrance_pointer
        self.index = index
        self.default_spawn = False


    def patch(self, patch: "KDL3ProcedurePatch", consumables: bool, local_items: bool, doors: bool, random: Random) -> None:
        patch.write_token(APTokenTypes.WRITE, self.pointer + 2, self.music.to_bytes(1, "little"))
        animals = [x for x in self.locations if "Animal" in x.name and x.item]
        if len(animals) > 0:
            for current_animal in animals:
                patch.write_token(APTokenTypes.WRITE, self.pointer + self.animal_pointers[current_animal.name] + 7,
                                  animal_map[current_animal.item.name].to_bytes(1, "little"))
        if local_items:
            for location in self.get_locations():
                if location.item is None or location.item.player != self.player:
                    continue
                item = location.item.code
                if item is None:
                    continue
                item_idx = item & 0x00000F
                location_idx = location.address & 0xFFFF
                if location_idx & 0xF00 in (0x300, 0x400, 0x500, 0x600):
                    # consumable or star, need remapped
                    location_base = location_idx & 0xF00
                    if location_base == 0x300:
                        # consumable
                        location_idx = consumable_addrs[location_idx & 0xFF] | 0x1000
                    else:
                        # star
                        location_idx = star_addrs[location.address] | 0x2000
                if item & 0x000070 == 0:
                    patch.write_token(APTokenTypes.WRITE, 0x4B000 + location_idx, bytes([item_idx | 0x10]))
                elif item & 0x000010 > 0:
                    patch.write_token(APTokenTypes.WRITE, 0x4B000 + location_idx, bytes([item_idx | 0x20]))
                elif item & 0x000020 > 0:
                    patch.write_token(APTokenTypes.WRITE, 0x4B000 + location_idx, bytes([item_idx | 0x40]))
                elif item & 0x000040 > 0:
                    patch.write_token(APTokenTypes.WRITE, 0x4B000 + location_idx, bytes([item_idx | 0x80]))

        if consumables:
            load_len = len(self.entity_load)
            for consumable in self.consumables:
                location = next(x for x in self.locations if x.name == consumable["name"])
                assert location.item is not None
                is_progression = location.item.classification & ItemClassification.progression
                if load_len == 8:
                    # edge case, there is exactly 1 room with 8 entities and only 1 consumable among them
                    if not (any(x in self.entity_load for x in [[0, 22], [1, 22]])
                            and any(x in self.entity_load for x in [[2, 22], [3, 22]])):
                        replacement_target = self.entity_load.index(
                            next(x for x in self.entity_load if x in [[0, 22], [1, 22], [2, 22], [3, 22]]))
                        if is_progression:
                            vtype = 0
                        else:
                            vtype = 2
                        patch.write_token(APTokenTypes.WRITE, self.pointer + 88 + (replacement_target * 2),
                                          vtype.to_bytes(1, "little"))
                        self.entity_load[replacement_target] = [vtype, 22]
                else:
                    if is_progression:
                        # we need to see if 1-ups are in our load list
                        if any(x not in self.entity_load for x in [[0, 22], [1, 22]]):
                            self.entity_load.append([0, 22])
                    else:
                        if any(x not in self.entity_load for x in [[2, 22], [3, 22]]):
                            # edge case: if (1, 22) is in, we need to load (3, 22) instead
                            if [1, 22] in self.entity_load:
                                self.entity_load.append([3, 22])
                            else:
                                self.entity_load.append([2, 22])
                if load_len < len(self.entity_load):
                    patch.write_token(APTokenTypes.WRITE, self.pointer + 88 + (load_len * 2),
                                      bytes(self.entity_load[load_len]))
                    patch.write_token(APTokenTypes.WRITE, self.pointer + 104 + (load_len * 2),
                                      bytes(struct.pack("H", self.consumable_pointer)))
                if is_progression:
                    if [1, 22] in self.entity_load:
                        vtype = 1
                    else:
                        vtype = 0
                else:
                    if [3, 22] in self.entity_load:
                        vtype = 3
                    else:
                        vtype = 2
                assert isinstance(consumable["pointer"], int)
                patch.write_token(APTokenTypes.WRITE, self.pointer + consumable["pointer"] + 7,
                                  vtype.to_bytes(1, "little"))

        if doors:
            door_ptr = self.entrance_pointer + self.pointer
            for exit_name in self.default_exits:
                exit_region = next((exit for exit in self.get_exits() if exit.name == exit_name), None)
                if not exit_region:
                    door_ptr += 10
                    continue  # one singular case, we filter out an unreachable entrance
                assert isinstance(exit_region, KDL3Door)
                target_coords = exit_region.connected_region.spawn if not exit_region.connected_region.default_spawn \
                    else random.choice(exit_region.connected_region.entrance_coords)
                patch.write_token(APTokenTypes.WRITE, door_ptr, exit_region.connected_region.index.to_bytes(2, "little"))
                patch.write_token(APTokenTypes.WRITE, door_ptr + 6, target_coords[0].to_bytes(2, "little"))
                patch.write_token(APTokenTypes.WRITE, door_ptr + 8, target_coords[1].to_bytes(2, "little"))
                door_ptr += 10
