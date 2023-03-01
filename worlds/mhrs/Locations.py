from .Quests import MR1Quests, MR2Quests, MR3Quests, MR4Quests, MR5Quests, MR6Quests
import typing
from BaseClasses import Location


class QuestData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str
    MR: int


class MHRSQuest(Location):
    game: str = "Monster Hunter Rise Sunbreak"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


# This is mostly for better logs
urgent_quests = {

}

mhr_quests = {
    MR1Quests[qid]: QuestData(qid, "MR1", 1) for qid in MR1Quests
}
mhr_quests.update({MR2Quests[qid]: QuestData(qid, "MR2", 2) for qid in MR2Quests})
mhr_quests.update({MR3Quests[qid]: QuestData(qid, "MR3", 3) for qid in MR3Quests})
mhr_quests.update({MR4Quests[qid]: QuestData(qid, "MR4", 4) for qid in MR4Quests})
mhr_quests.update({MR5Quests[qid]: QuestData(qid, "MR5", 5) for qid in MR5Quests})
mhr_quests.update({MR6Quests[qid]: QuestData(qid, "MR6", 6) for qid in MR6Quests})
mhr_quests.update({
    "1★ - Uninvited Guest": QuestData(315100, "MR1 Urgent", 1),
    "2★ - Scarlet Tengu in the Shrine Ruins": QuestData(315900, "MR1", 2),
    "3★ - A Rocky Rampage": QuestData(315901, "MR2", 3),
    "4★ - Ice Wolf, Red Moon": QuestData(315902, "MR3", 4),
    "5★ - Witness by Moonlight": QuestData(315903, "MR4", 5),
    "6★ - Proof of Courage": QuestData(315904, "MR5", 6)
})


def get_quest_table(mr: int):
    quests = [mhr_quests[quest].id for quest in mhr_quests if mhr_quests[quest].MR <= mr]
    return quests
