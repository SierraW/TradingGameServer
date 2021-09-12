from .Business import Business


class Construction(Business):
    class_name = "construction"

    def __init__(self,
                 name: str,
                 consume: dict,
                 required_structures: dict,
                 workforce: dict,
                 property_id: str = None,
                 base_charming: int = 0,
                 bonus_package: dict = None,
                 buffs: dict = None):
        self.consume = consume
        self.base_charming = base_charming
        self.bonus_package = bonus_package
        if buffs is None:
            self.buffs = dict()
        super().__init__(name=name, business_type=self.class_name,
                         required_structures=required_structures, property_id=property_id, workforce=workforce)

    @staticmethod
    def from_dict(source):
        construction = Construction(name=source['name'],
                                    consume=source['consume'],
                                    required_structures=source['required_structures'],
                                    workforce=source['workforce'],
                                    )
        if 'base_charming' in source:
            construction.base_charming = source['base_charming']
        if 'bonus_package' in source:
            construction.bonus_package = source['bonus_package']
        if 'buffs' in source:
            construction.buffs = source['buffs']
        return construction
