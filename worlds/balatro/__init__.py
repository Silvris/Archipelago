from NetUtils import SlotType
from worlds.AutoWorld import World, WebWorld
from BaseClasses import MultiWorld

class BalatroWorld(World):
    game = "Balatro"

    item_name_to_id = {
        "Nothing": -1
    }
    location_name_to_id = {
        "Cheat Console": -1,
        "Server": -2
    }

    def generate_early(self):
        self.multiworld.player_types[self.player] = SlotType.spectator  # mark as spectator