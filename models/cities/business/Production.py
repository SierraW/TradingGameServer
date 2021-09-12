from models.GameData import GameData
from models.Storage import Storage
from models.cities.business.Business import Business
from models.cities.property.Property import Property


class Production(Business):
    class_name = "production"

    def __init__(self,
                 name: str,
                 product: dict,
                 consume: dict,
                 required_structures: dict,
                 workforce: dict,
                 property_id: str = None,
                 base_charming: int = 0,
                 bonus_package: dict = None,
                 buffs: dict = None):
        self.product = product
        self.consume = consume
        self.base_charming = base_charming
        self.bonus_package = bonus_package
        if buffs is None:
            self.buffs = dict()
        super().__init__(name=name, business_type=self.class_name,
                         required_structures=required_structures, property_id=property_id, workforce=workforce)

    @staticmethod
    def from_dict(source):
        production = Production(name=source['name'],
                                product=source['product'],
                                consume=source['consume'],
                                required_structures=source['required_structures'],
                                workforce=source['workforce'],
                                )
        if 'base_charming' in source:
            production.base_charming = source['base_charming']
        if 'bonus_package' in source:
            production.bonus_package = source['bonus_package']
        if 'buffs' in source:
            production.buffs = source['buffs']
        return production
