import typing
from BaseClasses import Item


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    skip_balancing: bool = False
    trap: bool = False


class MHFUItem(Item):
    game = "Monster Hunter Freedom Unite"
