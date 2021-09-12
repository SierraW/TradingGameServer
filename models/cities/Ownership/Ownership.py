from models.TGTime import TGTime


# 0: ownership 1: property ~
class Ownership(object):
    def __init__(self, owner_financial_entity_id: str, start_date: TGTime,
                 end_date: TGTime = None,
                 parent=None):
        self.owner_financial_entity_id = owner_financial_entity_id
        self.start_date = start_date
        self.end_date = end_date
        self.parent = parent

    def ownership_type(self):
        return 0

    def is_valid(self, now: TGTime):
        if self.end_date is None:
            return True
        else:
            return self.end_date.less_than_or_equal_to(now)

    def is_original_owner(self):
        return self.parent is None
