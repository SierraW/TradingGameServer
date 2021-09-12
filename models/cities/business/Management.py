from .Business import Business


class Management(Business):
    class_name = "management"

    def __init__(self,
                 name: str,
                 required_structures: dict,
                 workforce: dict,
                 property_id: str = None,
                 bonus_package: dict = None,
                 buffs: dict = None):
        self.bonus_package = bonus_package
        if buffs is None:
            self.buffs = dict()
        super().__init__(name=name, business_type=self.class_name,
                         required_structures=required_structures, property_id=property_id, workforce=workforce)

    @staticmethod
    def from_dict(source):
        management = Management(name=source['name'],
                                required_structures=source['required_structures'],
                                workforce=source['workforce'],
                                )
        if 'bonus_package' in source:
            management.bonus_package = source['bonus_package']
        if 'buffs' in source:
            management.buffs = source['buffs']
        return management
