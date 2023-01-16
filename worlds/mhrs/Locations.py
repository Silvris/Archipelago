import worlds.mhrs.data.Quests as Quests
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
    Quests.MR1Quests[qid]: QuestData(qid, "MR1", 1) for qid in Quests.MR1Quests
}
mhr_quests.update({Quests.MR2Quests[qid]: QuestData(qid, "MR2", 2) for qid in Quests.MR2Quests})
mhr_quests.update({Quests.MR3Quests[qid]: QuestData(qid, "MR3", 3) for qid in Quests.MR3Quests})
mhr_quests.update({Quests.MR4Quests[qid]: QuestData(qid, "MR4", 4) for qid in Quests.MR4Quests})
mhr_quests.update({Quests.MR5Quests[qid]: QuestData(qid, "MR5", 5) for qid in Quests.MR5Quests})
mhr_quests.update({Quests.MR6Quests[qid]: QuestData(qid, "MR6", 6) for qid in Quests.MR6Quests})
# Final Quest
mhr_quests.update({"The Final Quest": QuestData(315905, "Final", -1)})


def get_exclusion_table(mr: int):
    excluded = set()
    if mr < 6:
        excluded.update({Quests.MR6Quests[qid] for qid in Quests.MR6Quests})
        if mr < 5:
            excluded.update({Quests.MR5Quests[qid] for qid in Quests.MR5Quests})
            if mr < 4:
                excluded.update({Quests.MR4Quests[qid] for qid in Quests.MR4Quests})
                if mr < 3:
                    excluded.update({Quests.MR3Quests[qid] for qid in Quests.MR3Quests})
                    if mr < 2:
                        excluded.update({Quests.MR2Quests[qid] for qid in Quests.MR2Quests})
    return excluded
