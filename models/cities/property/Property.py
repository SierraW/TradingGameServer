from models.Company import Company
from models.cities.property.Production import Production


class Property(object):
    def __init__(self, city_id, name):
        self.city_id = city_id
        self.name = name
        self.level = 1
        self.buffs = []

        self.financial_id = None
        self.storage_id = None
        self.production = None

    @staticmethod
    def from_dict(source):
        item = Property(source['city_id'], source['name'])
        if 'buffs' in source:
            item.buffs = source['buffs']
        if 'level' in source:
            item.level = Company.from_dict(source['level'])
        if 'financial_id' in source:
            item.company = source['financial_id']
        if 'storage_id' in source:
            item.storage_id = source['storage_id']
        if 'production' in source:
            item.production = Production.from_dict(source['production'])
        return item

    def to_dict(self):
        return {
            'city_id': self.city_id,
            'name': self.name,
            'level': self.level,
            'buffs': self.buffs,
            'financial_id': self.financial_id,
            'production': self.production.to_dict() if self.production is not None else None
        }

    def assign_production_task(self, production: Production):
        self.buffs = production.buffs
        self.production = production
