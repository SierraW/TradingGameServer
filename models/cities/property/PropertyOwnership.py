from models.TGTime import TGTime


# 0: ownership 1: property ~
class Ownership(object):
    def __init__(self, owner_financial_entity_id: str, start_date: TGTime,
                 end_date: TGTime):
        self.owner_financial_entity_id = owner_financial_entity_id
        self.start_date = start_date
        self.end_date = end_date

    def ownership_type(self):
        return 0

    def is_original_owner(self):
        return True


class PropertyOwnership(Ownership):
    def __init__(self, owner_financial_entity_id: str, start_date: TGTime,
                 end_date: TGTime, property_id: str,
                 rental_ownership: Ownership = None):
        super().__init__(owner_financial_entity_id, start_date, end_date)
        self.property_id = property_id
        self.rental_ownership = rental_ownership

    def is_original_owner(self):
        return self.rental_ownership is None

    def ownership_type(self):
        return 1
