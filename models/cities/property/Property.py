from models.cities.property.Production import Production
from models.cities.property.Structure import Structure


class Property(object):
    def __init__(self, city_id: str, name: str, financial_id: str, storage_id: str, storage_in_id: str = None, storage_out_id: str = None, production_template_id: str = None, production: Production = None, structure: Structure = None):
        self.city_id = city_id
        self.name = name
        self.financial_id = financial_id
        self.storage_id = storage_id

        self.storage_in_id = storage_in_id
        self.storage_out_id = storage_out_id
        self.production_template_id = production_template_id
        self.production = production
        self.structure = structure

        self.buffs = dict()
