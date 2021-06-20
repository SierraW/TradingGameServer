from models.Buff import Buff


def buff_loop(buffs: list[Buff]):
    index = 0
    while index < len(buffs):
        if buffs[index].effective_days_remaining is None:
            index += 1
        elif buffs[index].effective_days_remaining is 0:
            del buffs[index]
        else:
            buffs[index].effective_days_remaining += 1
