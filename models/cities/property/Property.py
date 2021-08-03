from models.Company import Company
from models.cities.property.Production import Production


class Property(object):
    def __init__(self, city_id, name, financial_id: str, storage_id: str, auto_managed: bool):
        self.city_id = city_id
        self.name = name
        self.buffs = dict()
        self.financial_id = financial_id
        self.storage_id = storage_id
        self.auto_managed = auto_managed

        self.storage_in_id = None
        self.storage_out_id = None
        self.auto_register_market_id = None
        self.production = None

    @staticmethod
    def from_dict(source):
        item = Property(source['city_id'], source['name'], source['financial_id'], auto_managed=source['auto_managed'],
                        storage_id=source['storage_id'])
        if 'buffs' in source:
            item.buffs = source['buffs']
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
            'auto_managed': self.auto_managed,
            'financial_id': self.financial_id,
            'storage_id': self.storage_id,
            'storage_in_id': self.storage_in_id,
            'storage_out_id': self.storage_out_id,
            'auto_register_market_id': self.auto_register_market_id,
            'production': self.production.to_dict() if self.production is not None else None
        }

    def __repr__(self):
        return self.to_dict().__repr__()
