import logging

import orjson
import os
from pkgutil import get_data
from copy import deepcopy

from typing import TYPE_CHECKING, List, Dict, Optional, Union, Callable
from BaseClasses import Region, CollectionState
from worlds.generic.Rules import add_item_rule
from .locations import KDL3Location, stage_locations, heart_star_locations, boss_locations
from .items import copy_ability_access_table
from .names import location_name
from .options import BossShuffle
from .room import KDL3Room, final_iceberg_rooms, required_paths, required_set, KDL3Door

if TYPE_CHECKING:
    from . import KDL3World

default_levels = {
    1: [0x770000, 0x770001, 0x770002, 0x770003, 0x770004, 0x770005, 0x770200],
    2: [0x770006, 0x770007, 0x770008, 0x770009, 0x77000A, 0x77000B, 0x770201],
    3: [0x77000C, 0x77000D, 0x77000E, 0x77000F, 0x770010, 0x770011, 0x770202],
    4: [0x770012, 0x770013, 0x770014, 0x770015, 0x770016, 0x770017, 0x770203],
    5: [0x770018, 0x770019, 0x77001A, 0x77001B, 0x77001C, 0x77001D, 0x770204],
}

stage_names = {stage: stage_locations[stage].replace(" - Complete", "") for stage in stage_locations}
stage_names.update({stage: boss_locations[stage].replace(" Purified", "") for stage in boss_locations})

first_stage_blacklist = {
    # We want to confirm that the first stage can be completed without any items
    0x77000A,  # 2-5 needs Kine
    0x770010,  # 3-5 needs Cutter
    0x77001B,  # 5-4 needs Burning
}

first_world_limit = {
    # We need to limit the number of very restrictive stages in level 1 on solo gens
    *first_stage_blacklist,  # all three of the blacklist stages need 2+ items for both checks
    0x770006,
    0x770007,
    0x770012,
    0x77001D,

}

door_shuffle_events = {
    "Grass Land 4 - 6-2": {location_name.grass_land_4_goku: "Goku"},
    "Ripple Field 4 - 2-1": {location_name.ripple_field_4_little_toad: "Little Toad"},
    "Ripple Field 5 - 8": {location_name.ripple_field_5_wall: "Wall"},
    "Sand Canyon 4 - 6-2": {location_name.sand_canyon_4_donbe: "Donbe"},
    "Cloudy Park 4 - 8": {location_name.cloudy_park_4_mikarin: "Mikarin"},
    "Iceberg 4 - 10-1": {location_name.iceberg_4_shell: "Shell"}
}

heart_star_requirement = {  # Rooms required for the current stage's heart star
    "Grass Land 1 - 3",
    "Grass Land 1 - 4",
    "Grass Land 1 - 5",
    "Grass Land 2 - 3",
    "Grass Land 2 - 5",
    "Grass Land 2 - 6",
    "Grass Land 3 - 3",
    "Grass Land 3 - 5",
    "Grass Land 3 - 7",
    "Grass Land 4 - 6-1",
    "Grass Land 4 - 6-2", # Actual Requirement
    "Grass Land 4 - 8",
    "Grass Land 4 - 10",
    "Grass Land 5 - 5",
    "Grass Land 5 - 6",
    "Grass Land 6 - 1",
    "Grass Land 6 - 5",
    "Grass Land 6 - 8",
    "Ripple Field 1 - 4",
    "Ripple Field 1 - 5",
    "Ripple Field 1 - 6",
    "Ripple Field 1 - 7",
    "Ripple Field 1 - 8",
    "Ripple Field 2 - 4",
    "Ripple Field 2 - 6",
    "Ripple Field 2 - 7",
    "Ripple Field 3 - 5",
    "Ripple Field 3 - 4",
    "Ripple Field 3 - 6",
    "Ripple Field 4 - 2-1",  # Actual requirement
    "Ripple Field 4 - 2-2",
    "Ripple Field 4 - 3",
    "Ripple Field 4 - 4",
    "Ripple Field 5 - 9",
    "Ripple Field 5 - 11",
    "Ripple Field 6 - 3",  # Questionable, needs testing. if fail add in 4 as well
    # "Ripple Field 6 - 4",
    "Ripple Field 6 - 10",
    "Ripple Field 6 - 11",
    "Sand Canyon 1 - 0",
    "Sand Canyon 1 - 7",
    "Sand Canyon 1 - 8",
    "Sand Canyon 2 - 6",
    # "Sand Canyon 2 - 7",  # unknown if needed currently
    "Sand Canyon 2 - 8",
    "Sand Canyon 2 - 10",
    "Sand Canyon 2 - 11",
    "Sand Canyon 3 - 5",
    "Sand Canyon 3 - 7",
    "Sand Canyon 3 - 8",
    "Sand Canyon 4 - 6-1",
    "Sand Canyon 4 - 6-2",  # Actual requirement
    "Sand Canyon 4 - 6-3",
    "Sand Canyon 4 - 8",
    "Sand Canyon 4 - 9",
    "Sand Canyon 5 - 7",
    "Sand Canyon 5 - 8",
    "Sand Canyon 6 - 15",
    "Sand Canyon 6 - 18",
    "Sand Canyon 6 - 20",
    "Sand Canyon 6 - 29",
    "Sand Canyon 6 - 37",
    "Sand Canyon 6 - 43",
    "Sand Canyon 6 - 44",
    "Cloudy Park 1 - 8",
    "Cloudy Park 1 - 12",
    "Cloudy Park 1 - 13",
    "Cloudy Park 2 - 7",
    "Cloudy Park 2 - 8",
    "Cloudy Park 2 - 9",
    "Cloudy Park 3 - 5",
    "Cloudy Park 3 - 6",
    "Cloudy Park 3 - 7",
    "Cloudy Park 4 - 8",
    "Cloudy Park 4 - 9",
    "Cloudy Park 4 - 10",
    "Cloudy Park 5 - 7",
    "Cloudy Park 5 - 8",
    # "Cloudy Park 6 - 13",
    "Cloudy Park 6 - 14",
    "Cloudy Park 6 - 15",
    "Cloudy Park 6 - 16",
    "Iceberg 1 - 2",
    "Iceberg 1 - 6",
    "Iceberg 1 - 7",
    "Iceberg 2 - 3",
    "Iceberg 2 - 4",
    "Iceberg 2 - 5",
    "Iceberg 2 - 8",
    "Iceberg 2 - 10",
    "Iceberg 3 - 5",
    "Iceberg 3 - 7",
    "Iceberg 3 - 8",
    "Iceberg 4 - 10-1",  # Actual Requirement
    "Iceberg 4 - 10-2",
    "Iceberg 4 - 19",
    "Iceberg 4 - 20",
    "Iceberg 5 - 36",
    "Iceberg 5 - 37",
    "Iceberg 6 - 8",
    "Iceberg 6 - 10",
    "Iceberg 6 - 12",
    "Iceberg 6 - 14",
    "Iceberg 6 - 16",
    "Iceberg 6 - 18",
    "Iceberg 6 - 20",
    "Iceberg 6 - 22",
    "Iceberg 6 - 23",
    "Iceberg 6 - 24",

    # Boss rooms
    "Grass Land Boss - 0",
    "Ripple Field Boss - 0",
    "Sand Canyon Boss - 0",
    "Cloudy Park Boss - 0",
    "Iceberg Boss - 0",
}

blocked_groups = {
    # this room is going to cause me nightmares
    "Sand Canyon 5 - 9": [4, 7, 11]  # Kine physically cannot make this jump
}

extra_connections = {  # Connections that exist but must be split for logic
    "Iceberg 4 - 15-1": {
        "Iceberg 4 - 15-2": lambda state, player: state.has_all(["Parasol", "Parasol Ability"], player),
        "Iceberg 4 - 15-3": lambda state, player: state.has_all(["Clean", "Clean Ability"], player),
    },
    "Iceberg 4 - 15-2": {
        "Iceberg 4 - 15-1": lambda state, player: state.has_all(["Parasol", "Parasol Ability"], player),
    },
    "Iceberg 4 - 15-3": {
        "Iceberg 4 - 15-1": lambda state, player: state.has_all(["Clean", "Clean Ability"], player),
    },
}

linked_rooms = {
    "Grass Land 4 - 6-1": ["Grass Land 4 - 6-2"],
    "Ripple Field 3 - 7-1": ["Ripple Field 3 - 7-2"],
    "Ripple Field 4 - 2-1": ["Ripple Field 4 - 2-2"],
    "Ripple Field 4 - 5-1": ["Ripple Field 4 - 5-2", "Ripple Field 4 - 5-3"],
    "Ripple Field 4 - 7-1": ["Ripple Field 4 - 7-2"],
    "Sand Canyon 2 - 4-1": ["Sand Canyon 2 - 4-2"],
    "Sand Canyon 2 - 5-1": ["Sand Canyon 2 - 5-2", "Sand Canyon 2 - 5-3", "Sand Canyon 2 - 5-4"],
    "Sand Canyon 3 - 1-1": ["Sand Canyon 3 - 1-2", "Sand Canyon 3 - 1-3"],
    "Sand Canyon 4 - 6-1": ["Sand Canyon 4 - 6-2", "Sand Canyon 4 - 6-3"],
    "Cloudy Park 6 - 4-1": ["Cloudy Park 6 - 4-2", "Cloudy Park 6 - 4-3", "Cloudy Park 6 - 4-4", "Cloudy Park 6 - 4-5"],
    "Cloudy Park 6 - 10-1": ["Cloudy Park 6 - 10-2", "Cloudy Park 6 - 10-3", "Cloudy Park 6 - 10-4", "Cloudy Park 6 - 10-5"],
    "Iceberg 4 - 10-1": ["Iceberg 4 - 10-2"],
    "Iceberg 4 - 13-1": ["Iceberg 4 - 13-2"],
    "Iceberg 4 - 14-1": ["Iceberg 4 - 14-2"],
    "Iceberg 4 - 15-1": ["Iceberg 4 - 15-2", "Iceberg 4 - 15-3"],
}


def generate_valid_level(world: "KDL3World", level: int, stage: int,
                         possible_stages: List[int], placed_stages: List[Optional[int]]) -> int:
    new_stage = world.random.choice(possible_stages)
    if level == 1:
        if stage == 0 and new_stage in first_stage_blacklist:
            possible_stages.remove(new_stage)
            return generate_valid_level(world, level, stage, possible_stages, placed_stages)
        elif (not (world.multiworld.players > 1 or world.options.consumables or world.options.starsanity) and
              new_stage in first_world_limit and
              sum(p_stage in first_world_limit for p_stage in placed_stages)
              >= (2 if world.options.open_world else 1)):
            return generate_valid_level(world, level, stage, possible_stages, placed_stages)
    return new_stage


def generate_rooms(world: "KDL3World", level_regions: Dict[int, Region]) -> None:
    level_names = {location_name.level_names[level]: level for level in location_name.level_names}
    room_data = orjson.loads(get_data(__name__, "data/Rooms.json"))
    rooms: Dict[str, KDL3Room] = dict()
    for room_entry in room_data:
        room = KDL3Room(room_entry["name"], world.player, world.multiworld, None, room_entry["level"],
                        room_entry["stage"], room_entry["room"], room_entry["pointer"], room_entry["music"],
                        room_entry["default_exits"], room_entry["animal_pointers"], room_entry["enemies"],
                        room_entry["entity_load"], room_entry["consumables"], room_entry["consumables_pointer"],
                        room_entry["entrances"], room_entry["spawn"], room_entry["index"])
        room.add_locations({location: world.location_name_to_id[location] if location in world.location_name_to_id else
        None for location in room_entry["locations"]
                            if (not any(x in location for x in ["1-Up", "Maxim"]) or
                                world.options.consumables.value) and ("Star" not in location
                                                                      or world.options.starsanity.value)},
                           KDL3Location)
        rooms[room.name] = room
        for location in room.locations:
            if "Animal" in location.name:
                add_item_rule(location, lambda item: item.name in {
                    "Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"
                })
    world.rooms = list(rooms.values())
    world.multiworld.regions.extend(world.rooms)

    first_rooms: Dict[int, KDL3Room] = dict()
    for name, room in rooms.items():
        if room.room == 0:
            if room.stage == 7:
                first_rooms[0x770200 + room.level - 1] = room
            else:
                first_rooms[0x770000 + ((room.level - 1) * 6) + room.stage - 1] = room
        for exit_name, def_exit in room.default_exits.items():
            target: str = def_exit["room"]
            access_rule = None
            if def_exit["access_rule"]:
                required_items = tuple(def_exit["access_rule"])
                access_rule = lambda state, rule=required_items: state.has_all(rule, world.player)
            room.connect(rooms[target], exit_name, access_rule)
        if world.options.open_world:
            if any("Complete" in location.name for location in room.locations):
                room.add_locations({f"{level_names[room.level]} {room.stage} - Stage Completion": None},
                                   KDL3Location)
        if room.name in door_shuffle_events:
            for location, item in door_shuffle_events[room.name].items():
                world.get_location(location).place_locked_item(world.create_item(item))

    for level in world.player_levels:
        for stage in range(6):
            proper_stage = world.player_levels[level][stage]
            stage_name = world.multiworld.get_location(world.location_id_to_name[proper_stage],
                                                       world.player).name.replace(" - Complete", "")
            stage_regions = [rooms[room] for room in rooms if stage_name in rooms[room].name]
            if not world.options.door_shuffle:
                for region in stage_regions:
                    region.level = level
                    region.stage = stage
            if world.options.open_world or stage == 0:
                level_regions[level].add_exits([first_rooms[proper_stage].name])
            else:
                world.multiworld.get_location(world.location_id_to_name[world.player_levels[level][stage - 1]],
                                              world.player).parent_region.add_exits([first_rooms[proper_stage].name])
        if world.options.open_world:
            level_regions[level].add_exits([first_rooms[0x770200 + level - 1].name])
        else:
            world.multiworld.get_location(world.location_id_to_name[world.player_levels[level][5]], world.player) \
                .parent_region.add_exits([first_rooms[0x770200 + level - 1].name])


def generate_valid_levels(world: "KDL3World", shuffle_mode: int) -> Dict[int, List[int]]:
    if shuffle_mode:
        levels: Dict[int, List[Optional[int]]] = {
            1: [None] * 7,
            2: [None] * 7,
            3: [None] * 7,
            4: [None] * 7,
            5: [None] * 7,
        }

        possible_stages = [default_levels[level][stage] for level in default_levels for stage in range(6)]
        if world.options.plando_connections:
            for connection in world.options.plando_connections:
                try:
                    entrance_world, entrance_stage = connection.entrance.rsplit(" ", 1)
                    stage_world, stage_stage = connection.exit.rsplit(" ", 1)
                    new_stage = default_levels[location_name.level_names[stage_world.strip()]][int(stage_stage) - 1]
                    levels[location_name.level_names[entrance_world.strip()]][int(entrance_stage) - 1] = new_stage
                    possible_stages.remove(new_stage)

                except Exception:
                    raise Exception(
                        f"Invalid connection: {connection.entrance} =>"
                        f" {connection.exit} for player {world.player} ({world.player_name})")

        for level in range(1, 6):
            for stage in range(6):
                # Randomize bosses separately
                if levels[level][stage] is None:
                    stage_candidates = [candidate for candidate in possible_stages
                                        if (shuffle_mode == 1 and candidate in default_levels[level])
                                        or (shuffle_mode == 2 and (candidate & 0x00FFFF) % 6 == stage)
                                        or (shuffle_mode == 3)
                                        ]
                    if not stage_candidates:
                        raise Exception(
                            f"Failed to find valid stage for {level}-{stage}. Remaining Stages:{possible_stages}")
                    new_stage = generate_valid_level(world, level, stage, stage_candidates, levels[level])
                    possible_stages.remove(new_stage)
                    levels[level][stage] = new_stage
    else:
        levels = deepcopy(default_levels)
        for level in levels:
            levels[level][6] = None
    # now handle bosses
    boss_shuffle: Union[int, str] = world.options.boss_shuffle.value
    plando_bosses = []
    if isinstance(boss_shuffle, str):
        # boss plando
        options = boss_shuffle.split(";")
        boss_shuffle = BossShuffle.options[options.pop()]
        for option in options:
            if "-" in option:
                loc, plando_boss = option.split("-")
                loc = loc.title()
                plando_boss = plando_boss.title()
                levels[location_name.level_names[loc]][6] = location_name.boss_names[plando_boss]
                plando_bosses.append(location_name.boss_names[plando_boss])
            else:
                option = option.title()
                for level in levels:
                    if levels[level][6] is None:
                        levels[level][6] = location_name.boss_names[option]
                        plando_bosses.append(location_name.boss_names[option])

    if boss_shuffle > 0:
        if boss_shuffle == BossShuffle.option_full:
            possible_bosses = [default_levels[world.random.randint(1, 5)][6]
                               for _ in range(5 - len(plando_bosses))]
        elif boss_shuffle == BossShuffle.option_singularity:
            boss = world.random.randint(1, 5)
            possible_bosses = [default_levels[boss][6] for _ in range(5 - len(plando_bosses))]
        else:
            possible_bosses = [default_levels[level][6] for level in default_levels
                               if default_levels[level][6] not in plando_bosses]
        for level in levels:
            if levels[level][6] is None:
                boss = world.random.choice(possible_bosses)
                levels[level][6] = boss
                possible_bosses.remove(boss)
    else:
        for level in levels:
            if levels[level][6] is None:
                levels[level][6] = default_levels[level][6]

    for level in levels:
        for stage in range(7):
            assert levels[level][stage] is not None, "Level tried to be sent with a None stage, incorrect plando?"

    return levels


def shuffle_doors(world: "KDL3World"):
    from Utils import visualize_regions
    linked_skip = []
    for value in linked_rooms.values():
        linked_skip.extend(value)
    non_randomized_rooms: List[str] = []
    randomized_rooms: List[KDL3Room] = []
    available_groups: List[int] = [default_levels[room.level][room.stage - 1] & 0xFF for room in world.rooms
                        if room.name not in heart_star_requirement and room.name not in linked_skip]
    group_match = {group: [group] for group in available_groups}
    world.random.shuffle(available_groups)

    for room in world.rooms:
        if any(location.address in stage_locations
               for location in room.get_locations()):
            non_randomized_rooms.append(room.name)

        elif any(location.address in boss_locations for location in room.get_locations()):
            non_randomized_rooms.append(room.name)

        elif room.name not in non_randomized_rooms:
            randomized_rooms.append(room)

    level_regions = [world.multiworld.get_region(x, world.player) for x in ["Grass Land", "Ripple Field", "Sand Canyon",
                                                                            "Cloudy Park", "Iceberg"]]

    from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances, EntranceRandomizationError

    randomized_entrances = []

    for room in randomized_rooms:
        randomized_entrances.extend(list(room.entrances))

    for entrance in randomized_entrances:
        disconnect_entrance_for_randomization(entrance, one_way_target_name=entrance.connected_region.name)
        # have to place groups later

    local_rooms = world.rooms.copy()
    world.random.shuffle(local_rooms)
    exits = []
    entrances = []

    def define_randomization_group(room: KDL3Room, stage_group: int):
        room.level = (stage_group // 6) + 1
        room.stage = (stage_group % 6) + 1

        for exit in room.get_exits():
            exit.randomization_group = stage_group

        for entrance in room.entrances:
            entrance.randomization_group = stage_group

        if room.name in linked_rooms:
            for region in linked_rooms[room.name]:
                r_room = world.get_region(region)
                for r_exit in r_room.get_exits():
                    r_exit.randomization_group = stage_group

                for r_entrance in r_room.entrances:
                    r_entrance.randomization_group = stage_group
                exits.extend(list(r_room.get_exits()))
                entrances.extend(list(r_room.entrances))

    for iceberg, ability in final_iceberg_rooms.items():
        # Iceberg 6 special handling
        # We have to make a special pool here
        room = world.get_region(iceberg)
        assert isinstance(room, KDL3Room)
        handled_room = next((room for room in local_rooms if
                            any(world.copy_abilities[enemy] == ability for enemy in room.enemies) and
                            room.name not in linked_skip and room.name not in heart_star_requirement), None)
        if not handled_room:
            # throw proper exception, shouldnt ever reach this
            raise Exception("Unable to resolve Iceberg 6 rooms.")
        local_rooms.remove(room)
        local_rooms.remove(handled_room)
        stage_group = 29
        available_groups.remove(stage_group)

        define_randomization_group(room, stage_group)
        define_randomization_group(handled_room, stage_group)

        # Now grab an entrance to Iceberg 6 and an exit from the handled room
        source_exit = world.random.choice(handled_room.get_exits())
        target_entrance = world.random.choice(room.entrances)

        room.entrances.remove(target_entrance)
        source_exit.connect(room)

        exits.extend(list(handled_room.get_exits()))
        entrances.extend(list(handled_room.entrances))
        exits.extend(list(room.get_exits()))
        entrances.extend(list(room.entrances))

    for room in local_rooms:
        if room.name in non_randomized_rooms or room.name in linked_skip:
            continue
        if room.name not in heart_star_requirement:
            stage_group = available_groups.pop()

        else:
            stage_group = default_levels[room.level][room.stage - 1] & 0xFF

        define_randomization_group(room, stage_group)

        exits.extend(list(room.get_exits()))
        entrances.extend(list(room.entrances))

    er_targets = []
    er_exits = []
    groups = {}

    for group, stage in stage_names.items():
        group = group & 0xFF
        groups[group] = ([x for x in entrances if x.randomization_group == group and x.parent_region is None],
                         [x for x in exits if x.randomization_group == group and x.connected_region is None])

    for i, region in enumerate(level_regions, 1):
        for j in range(6):
            stage = world.player_levels[i][j]
            stage_name = stage_names[stage]
            entrance = world.get_entrance(f"{region.name} -> {stage_name} - 0")
            entrance.randomization_group = stage & 0xFF
            groups[stage & 0xFF][1].append(entrance)

    for group in groups:
        g_entrances = groups[group][0]
        g_exits = groups[group][1]
        if len(g_entrances) > len(g_exits):
            # too many entrances
            unique_entrances = {x.name for x in g_entrances}
            while len(g_entrances) > len(g_exits):
                potential = g_entrances.pop()
                if unique_entrances == {x.name for x in g_entrances}:
                    # this is safe to remove
                    potential.connected_region.entrances.remove(potential)
                else:
                    # last entrance to the region, keep
                    g_entrances.insert(0, potential)

        elif len(g_entrances) < len(g_exits):
            possible_entrances: List[Region] = [x.connected_region for x in g_entrances if x.connected_region]
            while len(g_entrances) < len(g_exits):
                region = world.random.choice(possible_entrances)
                new_entrance = region.create_er_target(region.name)
                new_entrance.randomization_group = group
                region.entrances.append(new_entrance)
                g_entrances.append(new_entrance)
    for idx, group in groups.items():
        er_targets.extend(group[0])
        er_exits.extend(group[1])

    def find_nearest_entrance(room: KDL3Room, world: "KDL3World"):
        if any(entrance for entrance in room.entrances if not entrance.parent_region):
            return world.random.choice([en for en in room.entrances if not en.parent_region])
        elif not any(entrance for entrance in room.entrances if isinstance(entrance, KDL3Door)):
            raise Exception("Catastrophic failure in KDL3 Door Shuffle")
        else:
            # just travel up first entrance with parent
            entrances = [entrance for entrance in room.entrances if entrance.parent_region]
            return find_nearest_entrance(entrances[0].parent_region, world)

    for group, goal in zip(required_set, required_paths):
        if group == 29:
            continue # the way this level's special case has to be done, it can never actually hit this issue
        goal_region = world.get_region(goal)
        entrances, exits = groups[group]
        # don't have to shuffle entrances, we only pop from them
        found_regions = []
        required_regions = required_set[group]
        room = goal_region
        while not all(region in found_regions for region in required_regions):
            distance = world.random.randint(1, 4)
            while distance:
                # should be safe, since we break if a required gets hit
                exit: KDL3Door = world.random.choice([ex for ex in exits if isinstance(ex, KDL3Door)
                                                      and ex.parent_region.name not in found_regions])
                exits.remove(exit)
                entrance = find_nearest_entrance(room, world)
                room = entrance.connected_region
                room.entrances.remove(entrance)
                entrances.remove(entrance)
                exit.connected_region = room
                distance -= 1
                room = exit.parent_region
                found_regions.append(room.name)
                if room.name in required_regions:
                    break
            if not all(region in found_regions for region in required_regions):
                # manually place the required
                req_regions = sorted(required_regions.difference(found_regions))
                world.random.shuffle(req_regions)
                req = req_regions.pop()
                req_reg = world.get_region(req)
                exit: KDL3Door = world.random.choice([ex for ex in req_reg.get_exits() if not ex.connected_region])
                exit.connected_region = room
                exits.remove(exit)
                entrance = find_nearest_entrance(room, world)
                room.entrances.remove(entrance)
                entrances.remove(entrance)
                found_regions.append(req)
                room = req_reg

    for i in range(1, 6):
        for j in range(6):
            group = groups[world.player_levels[i][j] & 0xFF]
            retries = 10
            while retries > 0:
                try:
                    randomize_entrances(world, False, group_match, False, group[0], group[1])
                    break
                except EntranceRandomizationError:
                    logging.error(f"{world.player_name} ER failed for group {group[0][0].randomization_group}."
                                  f" {retries} retries remaining.")
                    retries -= 1
                    if not retries:
                        raise


    visualize_regions(world.multiworld.get_region("Menu", world.player), "kdl3_doors.puml", show_locations=False)
    #raise NotImplementedError


def create_levels(world: "KDL3World") -> None:
    menu = Region("Menu", world.player, world.multiworld)
    level1 = Region("Grass Land", world.player, world.multiworld)
    level2 = Region("Ripple Field", world.player, world.multiworld)
    level3 = Region("Sand Canyon", world.player, world.multiworld)
    level4 = Region("Cloudy Park", world.player, world.multiworld)
    level5 = Region("Iceberg", world.player, world.multiworld)
    level6 = Region("Hyper Zone", world.player, world.multiworld)
    levels = {
        1: level1,
        2: level2,
        3: level3,
        4: level4,
        5: level5,
    }
    level_shuffle = world.options.stage_shuffle.value
    if hasattr(world.multiworld, "re_gen_passthrough"):
        world.player_levels = getattr(world.multiworld, "re_gen_passthrough")["Kirby's Dream Land 3"]["player_levels"]
    else:
        world.player_levels = generate_valid_levels(world, level_shuffle)

    menu.connect(level1, "Start Game")
    level1.connect(level2, "To Level 2")
    level2.connect(level3, "To Level 3")
    level3.connect(level4, "To Level 4")
    level4.connect(level5, "To Level 5")
    menu.connect(level6, "To Level 6")  # put the connection on menu, since you can reach it before level 5 on fast goal
    world.multiworld.regions += [menu, level1, level2, level3, level4, level5, level6]

    generate_rooms(world, levels)

    level6.add_locations({location_name.goals[world.options.goal.value]: None}, KDL3Location)