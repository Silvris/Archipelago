import json
import os
import typing
from pkgutil import get_data

import Utils
from BaseClasses import Region
from worlds.generic.Rules import add_item_rule
from .Locations import KDL3Location, heart_star_locations, stage_locations, boss_locations
from .Names import LocationName
from .Options import BossShuffle
from .Room import KDL3Room

if typing.TYPE_CHECKING:
    from . import KDL3World

default_levels = {
    1: [0x770001, 0x770002, 0x770003, 0x770004, 0x770005, 0x770006, 0x770200],
    2: [0x770007, 0x770008, 0x770009, 0x77000A, 0x77000B, 0x77000C, 0x770201],
    3: [0x77000D, 0x77000E, 0x77000F, 0x770010, 0x770011, 0x770012, 0x770202],
    4: [0x770013, 0x770014, 0x770015, 0x770016, 0x770017, 0x770018, 0x770203],
    5: [0x770019, 0x77001A, 0x77001B, 0x77001C, 0x77001D, 0x77001E, 0x770204],
}

stage_names = {stage: stage_locations[stage].replace(" - Complete", "") for stage in stage_locations}
stage_names.update({stage: boss_locations[stage].replace(" Purified", "") for stage in boss_locations})

first_stage_blacklist = {
    0x77000B,  # 2-5 needs Kine
    0x770011,  # 3-5 needs Cutter
    0x77001C,  # 5-4 needs Burning
}

door_shuffle_events = {
    "Grass Land 4 - 6-2": {LocationName.grass_land_4_goku: None},
    "Ripple Field 4 - 2-1": {LocationName.ripple_field_4_little_toad: None},
    "Ripple Field 5 - 8": {LocationName.ripple_field_5_wall: None},
    "Sand Canyon 4 - 6-2": {LocationName.sand_canyon_4_donbe: None},
    "Cloudy Park 4 - 8": {LocationName.cloudy_park_4_mikarin: None},
    "Iceberg 4 - 10-1": {LocationName.iceberg_4_shell: None}

}

heart_star_requirement = {  # Rooms required for the current stage's heart star
    "Grass Land 1 - 3",
    "Grass Land 1 - 4",
    "Grass Land 1 - 5",
    "Grass Land 2 - 3",
    "Grass Land 2 - 5",
    "Grass Land 2 - 6"
    "Grass Land 3 - 3",
    "Grass Land 3 - 6",
    "Grass Land 3 - 5",
    "Grass Land 4 - 6-2",
    "Grass Land 4 - 8",
    "Grass Land 4 - 10",
    "Grass Land 5 - 5",
    "Grass Land 5 - 6"
    "Grass Land 6 - 1",
    "Grass Land 6 - 5",
    "Grass Land 6 - 8",
    "Ripple Field 1 - 5",
    "Ripple Field 1 - 6",
    "Ripple Field 1 - 7",
    "Ripple Field 2 - 4",
    "Ripple Field 2 - 6",
    "Ripple Field 2 - 7",
    "Ripple Field 3 - 5",
    "Ripple Field 3 - 4",
    "Ripple Field 3 - 6",
    "Ripple Field 4 - 2-1",
    "Ripple Field 4 - 3",
    "Ripple Field 4 - 4",
    "Ripple Field 5 - 9",
    "Ripple Field 5 - 11",
    "Ripple Field 6 - 3",  # Questionable, needs testing. if fail add in 4 as well
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
    "Sand Canyon 4 - 6-2",
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
    "Iceberg 4 - 10-1",
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
    "Iceberg Boss - 0"
}

blocked_groups = {
    # this room is going to cause me nightmares
    "Sand Canyon 5 - 9": ["Grass Land 5", "Ripple Field 2", "Sand Canyon 6"]  # Kine physically cannot make this jump
}


def generate_valid_level(level, stage, possible_stages, slot_random):
    new_stage = slot_random.choice(possible_stages)
    if level == 1 and stage == 0 and new_stage in first_stage_blacklist:
        return generate_valid_level(level, stage, possible_stages, slot_random)
    else:
        return new_stage


def generate_rooms(world: "KDL3World", level_regions: typing.Dict[int, Region]):
    level_names = {LocationName.level_names[level]: level for level in LocationName.level_names}
    room_data = json.loads(get_data(__name__, os.path.join("data", "Rooms.json")))
    rooms: typing.Dict[str, KDL3Room] = dict()
    for room_entry in room_data:
        if room_entry["name"] in split_rooms:
            for i in range(len(room_entry["default_exits"])):
                room = KDL3Room(room_entry["name"] + f"-{i + 1}", world.player, world.multiworld, None, room_entry["level"],
                                room_entry["stage"], room_entry["room"], room_entry["pointer"], room_entry["music"],
                                [room_entry["default_exits"][i]], room_entry["animal_pointers"], room_entry["enemies"],
                                room_entry["entity_load"], room_entry["consumables"], room_entry["consumables_pointer"])
                if room.name in heart_star_requirement:
                    room.add_locations(
                        {location: world.location_name_to_id[location] if location in world.location_name_to_id else
                        None for location in room_entry["locations"]
                         if (not any([x in location for x in ["1-Up", "Maxim"]]) or
                             world.options.consumables.value) and (
                                 not "Star" in location or world.options.starsanity.value)},
                        KDL3Location)
                elif len(room_entry["locations"]) > i and not any(room_entry["name"] == x[:-2]
                                                                      for x in heart_star_requirement):
                    room.add_locations({room_entry["locations"][i]:
                                            world.location_name_to_id[room_entry["locations"][i]]
                                            if room_entry["locations"][i] in world.location_name_to_id else None})
                rooms[room.name] = room
                for location in room.locations:
                    if "Animal" in location.name:
                        add_item_rule(location, lambda item: item.name in {
                            "Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"
                        })
        else:
            room = KDL3Room(room_entry["name"], world.player, world.multiworld, None, room_entry["level"],
                            room_entry["stage"], room_entry["room"], room_entry["pointer"], room_entry["music"],
                            room_entry["default_exits"], room_entry["animal_pointers"], room_entry["enemies"],
                            room_entry["entity_load"], room_entry["consumables"], room_entry["consumables_pointer"])
            room.add_locations({location: world.location_name_to_id[location] if location in world.location_name_to_id else
            None for location in room_entry["locations"]
                                if (not any([x in location for x in ["1-Up", "Maxim"]]) or
                                    world.options.consumables.value) and (
                                        not "Star" in location or world.options.starsanity.value)},
                               KDL3Location)
            rooms[room.name] = room
            for location in room.locations:
                if "Animal" in location.name:
                    add_item_rule(location, lambda item: item.name in {
                        "Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"
                    })
    world.rooms = [rooms[room] for room in rooms]
    world.multiworld.regions.extend(world.rooms)

    first_rooms: typing.Dict[int, KDL3Room] = dict()
    for name in rooms:
        room = rooms[name]
        if room.room == 0:
            if room.stage == 7:
                first_rooms[0x770200 + room.level - 1] = room
            else:
                first_rooms[0x770000 + ((room.level - 1) * 6) + room.stage] = room
        exits = dict()
        names = dict()
        for def_exit in room.default_exits:
            target = f"{level_names[room.level]} {room.stage} - {def_exit['room']}"
            access_rule = tuple(def_exit["access_rule"])
            exits[target] = lambda state, rule=access_rule: state.has_all(rule, world.player)
            names[target] = def_exit["name"]
        room.add_exits(
            names,
            exits
        )
        for exit in room.get_exits():
            exit.er_group = stage_names[default_levels[room.level][room.stage]]
        if world.options.open_world:
            if any(["Complete" in location.name for location in room.locations]):
                room.add_locations({f"{level_names[room.level]} {room.stage} - Stage Completion": None},
                                   KDL3Location)

    for level in world.player_levels:
        for stage in range(6):
            proper_stage = world.player_levels[level][stage]
            if world.options.open_world or stage == 0:
                level_regions[level].add_exits([first_rooms[proper_stage].name])
            else:
                previous_stage = first_rooms[world.player_levels[level][stage - 1]]
                world.multiworld.get_location(f"{level_names[previous_stage.level]} {previous_stage.stage}"
                                              f" - Complete", world.player) \
                    .parent_region.add_exits([first_rooms[proper_stage].name])
        else:
            level_regions[level].add_exits([first_rooms[0x770200 + level - 1].name])


def generate_valid_levels(world: "KDL3World", enforce_world: bool, enforce_pattern: bool) -> dict:
    levels: typing.Dict[int, typing.List[typing.Optional[int]]] = {
        1: [None for _ in range(7)],
        2: [None for _ in range(7)],
        3: [None for _ in range(7)],
        4: [None for _ in range(7)],
        5: [None for _ in range(7)]
    }

    possible_stages = list()
    for level in default_levels:
        for stage in range(6):
            possible_stages.append(default_levels[level][stage])

    if world.multiworld.plando_connections[world.player]:
        for connection in world.multiworld.plando_connections[world.player]:
            try:
                entrance_world, entrance_stage = connection.entrance.rsplit(" ", 1)
                stage_world, stage_stage = connection.exit.rsplit(" ", 1)
                new_stage = default_levels[LocationName.level_names[stage_world.strip()]][int(stage_stage) - 1]
                levels[LocationName.level_names[entrance_world.strip()]][int(entrance_stage) - 1] = new_stage
                possible_stages.remove(new_stage)

            except Exception:
                raise Exception(
                    f"Invalid connection: {connection.entrance} =>"
                    f" {connection.exit} for player {world.player} ({world.player_name})")

    for level in range(1, 6):
        for stage in range(6):
            # Randomize bosses separately
            try:
                if levels[level][stage] is None:
                    stage_candidates = [candidate for candidate in possible_stages
                                        if (enforce_world and candidate in default_levels[level])
                                        or (enforce_pattern and ((candidate - 1) & 0x00FFFF) % 6 == stage)
                                        or (enforce_pattern == enforce_world)
                                        ]
                    new_stage = generate_valid_level(level, stage, stage_candidates,
                                                     world.random)
                    possible_stages.remove(new_stage)
                    levels[level][stage] = new_stage
            except Exception:
                raise Exception(f"Failed to find valid stage for {level}-{stage}. Remaining Stages:{possible_stages}")

    # now handle bosses
    boss_shuffle: typing.Union[int, str] = world.options.boss_shuffle.value
    plando_bosses = []
    if isinstance(boss_shuffle, str):
        # boss plando
        options = boss_shuffle.split(";")
        boss_shuffle = BossShuffle.options[options.pop()]
        for option in options:
            if "-" in option:
                loc, boss = option.split("-")
                loc = loc.title()
                boss = boss.title()
                levels[LocationName.level_names[loc]][6] = LocationName.boss_names[boss]
                plando_bosses.append(LocationName.boss_names[boss])
            else:
                option = option.title()
                for level in levels:
                    if levels[level][6] is None:
                        levels[level][6] = LocationName.boss_names[option]
                        plando_bosses.append(LocationName.boss_names[option])

    if boss_shuffle > 0:
        if boss_shuffle == 2:
            possible_bosses = [default_levels[world.random.randint(1, 5)][6]
                               for _ in range(5 - len(plando_bosses))]
        elif boss_shuffle == 3:
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
    non_randomized_rooms = []
    randomized_rooms = []
    available_groups = [stage_names[default_levels[room.level][room.stage - 1]] for room in world.rooms
                        if room.name not in heart_star_requirement]
    world.random.shuffle(available_groups)
    for room in world.rooms:
        if any(location.address in heart_star_locations
               for location in room.get_locations()):
            for exit in room.get_exits():
                non_randomized_rooms.append(exit.connected_region.name)
            randomized_rooms.append(room)
        elif any(location.address in boss_locations for location in room.get_locations()):
            non_randomized_rooms.append(room.name)
        elif room.name not in non_randomized_rooms:
            randomized_rooms.append(room)

    level_regions = [world.multiworld.get_region(x, world.player) for x in ["Grass Land", "Ripple Field", "Sand Canyon",
                                                                            "Cloudy Park", "Iceberg"]]

    from EntranceRando import disconnect_entrances_for_randomization, randomize_entrances
    randomized_entrances = []
    for room in randomized_rooms:
        randomized_entrances.extend(list(room.entrances))
    disconnect_entrances_for_randomization(world, randomized_entrances)
    local_rooms = world.rooms.copy()
    world.random.shuffle(local_rooms)
    exits = []
    entrances = []
    for room in local_rooms:
        if room.name not in heart_star_requirement:
            stage_group = available_groups.pop()
        else:
            stage_group = stage_names[default_levels[room.level][room.stage - 1]]
        for exit in room.get_exits():
            exit.er_group = stage_group
        for entrance in room.entrances:
            entrance.er_group = stage_group
        exits.extend(list(room.get_exits()))
        entrances.extend(list(room.entrances))
    for region in level_regions:
        for exit in region.get_exits():
            if exit.connected_region not in level_regions:
                exit.er_group = exit.name.replace(f"{region.name} -> ", "").replace(" - 0", "")
                exits.append(exit)

    def group_match(group: str) -> typing.List[str]:
        return [group]
    groups = {}
    for stage, group in stage_names.items():
        groups[group] = ([x for x in entrances if x.er_group == group], [x for x in exits if x.er_group == group])
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
            possible_entrances = [x.connected_region for x in g_entrances]
            while len(g_entrances) < len(g_exits):
                region = world.random.choice(possible_entrances)
                new_entrance = region.create_er_target(region.name)
                new_entrance.er_group = group
                g_entrances.append(new_entrance)


    result = randomize_entrances(world, world.multiworld.get_regions(world.player), True, group_match, True)
    Utils.visualize_regions(world.multiworld.get_region("Menu", world.player), "kdl3_doors.puml", show_locations=False)
    raise NotImplementedError


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
    if level_shuffle != 0:
        world.player_levels = generate_valid_levels(
            world,
            level_shuffle == 1,
            level_shuffle == 2)
    menu.connect(level1, "Start Game")
    level1.connect(level2, "To Level 2")
    level2.connect(level3, "To Level 3")
    level3.connect(level4, "To Level 4")
    level4.connect(level5, "To Level 5")
    menu.connect(level6, "To Level 6")  # put the connection on menu, since you can reach it before level 5 on fast goal
    world.multiworld.regions += [menu, level1, level2, level3, level4, level5, level6]
    generate_rooms(world, levels)

    level6.add_locations({LocationName.goals[world.options.goal]: None}, KDL3Location)
