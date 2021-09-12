from models.cities.property.BonusPackage import BonusPackage


class Structure(object):
    def __init__(self, name: str, construction: dict,
                 bonus_package: BonusPackage,
                 storage_space: int,
                 unit_name_and_property_id_dict: dict = None,
                 charming: int = None):
        self.name = name
        self.construction = construction
        self.bonus_package = bonus_package

        self.unit_name_and_property_id_dict = unit_name_and_property_id_dict

        self.storage_space = storage_space
        self.charming = charming

    @staticmethod
    def from_dict(source):
        structure = Structure(name=source['name'], construction=source['construction'],
                              storage_space=source['storage_space'],
                              bonus_package=BonusPackage.from_dict(source['bonus_package']))
        if 'unit_name_and_property_id_dict' in source:
            structure.unit_name_and_property_id_dict = source['unit_name_and_property_id_dict']
        if 'charming' in source:
            structure.charming = source['charming']
        return structure

    def is_completed(self) -> bool:
        return self.construction['complete']
