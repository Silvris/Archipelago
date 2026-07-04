from BaseClasses import Item, ItemClassification
from typing import NamedTuple


class ItemData(NamedTuple):
    id: int
    classification: ItemClassification
    count: int = 1
