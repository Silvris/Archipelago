from BaseClasses import Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld


class DMC5WebWorld(WebWorld):
    theme = "stone"


class DMC5World(World):
    game = "Devil May Cry 5"
    # options_dataclass: DMC5Options
    # options: DMC5Options
    web = DMC5WebWorld()

