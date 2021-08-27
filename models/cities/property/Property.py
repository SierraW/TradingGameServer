from models.cities.property.Production import Production
from models.cities.property.Structure import Structure


class Property(object):
    def __init__(self, city_id: str, name: str, financial_id: str, size: int,
                 work_contract_id_list=None,
                 parent_property_id: str = None,
                 structure: Structure = None):
        if work_contract_id_list is None:
            work_contract_id_list = []
        self.city_id = city_id
        self.name = name
        self.financial_id = financial_id
        self.work_contract_id_list = work_contract_id_list


        self.structure = structure

        self.size = size
        self.parent_property_id = parent_property_id

        self.buffs = dict()
