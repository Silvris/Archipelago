from .Quests import MR1Quests, MR2Quests, MR3Quests, MR4Quests, MR5Quests, MR6Quests
import typing
from BaseClasses import Location


class QuestData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str
    MR: int
    urgent: bool = False


class MHRSQuest(Location):
    game: str = "Monster Hunter Rise Sunbreak"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)


urgent_quests = {
    "1★ - Uninvited Guest": QuestData(315100, "MR1 Urgent", 1, True),
    "2★ - Scarlet Tengu in the Shrine Ruins": QuestData(315900, "Master Rank 1", 2, True),
    "3★ - A Rocky Rampage": QuestData(315901, "Master Rank 2", 3, True),
    "4★ - Ice Wolf, Red Moon": QuestData(315902, "Master Rank 3", 4, True),
    "5★ - Witness by Moonlight": QuestData(315903, "Master Rank 4", 5, True),
    "6★ - Proof of Courage": QuestData(315904, "Master Rank 5", 6, True)
}

mhr_quests = {
    MR1Quests[qid]: QuestData(qid, "Master Rank 1", 1) for qid in MR1Quests
}
mhr_quests.update({MR2Quests[qid]: QuestData(qid, "Master Rank 2", 2) for qid in MR2Quests})
mhr_quests.update({MR3Quests[qid]: QuestData(qid, "Master Rank 3", 3) for qid in MR3Quests})
mhr_quests.update({MR4Quests[qid]: QuestData(qid, "Master Rank 4", 4) for qid in MR4Quests})
mhr_quests.update({MR5Quests[qid]: QuestData(qid, "Master Rank 5", 5) for qid in MR5Quests})
mhr_quests.update({MR6Quests[qid]: QuestData(qid, "Master Rank 6", 6) for qid in MR6Quests})
mhr_quests.update(urgent_quests)
mhr_quests.update({
    f"MR {urgent_quests[quest].MR} Urgent": QuestData(None, urgent_quests[quest].region, urgent_quests[quest].MR, True)
    for quest in urgent_quests
})


def get_quest_table(mr: int):
    quests = [mhr_quests[quest].id
              for quest in mhr_quests
              if mhr_quests[quest].id
              and mhr_quests[quest].MR <= mr]
    return quests


def get_mr_quest_num(mr: int) -> int:
    num = 0
    for quest in mhr_quests:
        if mhr_quests[quest].MR == mr and not mhr_quests[quest].urgent:
            num += 1
    return num
