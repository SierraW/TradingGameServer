from models.TGTime import TGTime
from models.cities.Ownership.Ownership import Ownership


class StockOwnership(Ownership):
    def __init__(self, owner_financial_entity_id: str, start_date: TGTime,
                 company_id: str,
                 amount: int,
                 tradable: bool,
                 end_date: TGTime = None,
                 parent: Ownership = None):
        super().__init__(owner_financial_entity_id, start_date, end_date, parent=parent)
        self.company_id = company_id
        self.amount = amount
        self.tradable = tradable
