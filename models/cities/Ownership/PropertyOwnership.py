from models.TGTime import TGTime
from models.cities.Ownership.Ownership import Ownership


class PropertyOwnership(Ownership):
    def __init__(self, owner_financial_entity_id: str, start_date: TGTime,
                 property_id: str,
                 end_date: TGTime = None,
                 parent: Ownership = None):
        super().__init__(owner_financial_entity_id, start_date, end_date, parent=parent)
        self.property_id = property_id

    def ownership_type(self):
        return 1
