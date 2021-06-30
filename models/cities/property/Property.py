from models.Company import Company
from models.cities.property.Production import Production


class Property(object):
    def __init__(self, city_id, name, financial_id: str):
        self.city_id = city_id
        self.name = name
        self.buffs = dict()
        self.financial_id = financial_id
        self.auto_management = False

        self.storage_in_id = None
        self.storage_out_id = None
        self.auto_register_market_id = None
        self.production = None

    @staticmethod
    def from_dict(source):
        item = Property(source['city_id'], source['name'], source['financial_id'])
        if 'buffs' in source:
            item.buffs = source['buffs']
        if 'auto_management' in source:
            item.auto_management = source['auto_management']
        if 'financial_id' in source:
            item.company = source['financial_id']
        if 'storage_in_id' in source:
            item.storage_in_id = source['storage_in_id']
        if 'storage_out_id' in source:
            item.storage_out_id = source['storage_out_id']
        if 'auto_register_market_id' in source:
            item.storage_in_id = source['auto_register_market_id']
        if 'production' in source:
            item.production = Production.from_dict(source['production'])
        return item

    def to_dict(self):
        return {
            'city_id': self.city_id,
            'name': self.name,
            'buffs': self.buffs,
            'auto_management': self.auto_management,
            'financial_id': self.financial_id,
            'storage_in_id': self.storage_in_id,
            'storage_out_id': self.storage_out_id,
            'auto_register_market_id': self.auto_register_market_id,
            'production': self.production.to_dict() if self.production is not None else None
        }

    def assign_production_task(self, production: Production, storage_in_id: str = None, storage_out_id: str = None,
                               auto_register_market_id: str = None):
        self.buffs = production.buffs
        self.production = production
        self.storage_in_id = storage_in_id
        self.storage_out_id = storage_out_id
        self.auto_register_market_id = auto_register_market_id
