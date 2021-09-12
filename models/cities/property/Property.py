from models.cities.business.Business import Business
from models.cities.property.Structure import Structure


class Property(object):
    def __init__(self, city_id: str, serial_name: str, name: str, financial_id: str, size: int,
                 work_contract_id_list: list = None,
                 parent_property_id: str = None,
                 structure_id: str = None,
                 structure: Structure = None,
                 business: Business = None):
        if work_contract_id_list is None:
            work_contract_id_list = []
        self.city_id = city_id
        self.serial_name = serial_name
        self.name = name
        self.financial_id = financial_id
        self.work_contract_id_list = work_contract_id_list

        self.structure_id = structure_id
        self.structure = structure
        self.business = business

        self.size = size
        self.parent_property_id = parent_property_id

        self.buffs = dict()
