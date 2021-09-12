import debug_toolkit
from models.Storage import Storage


class Business(object):
    def __init__(self,
                 name: str,
                 business_type: str,
                 required_structures: dict,
                 workforce: dict,
                 property_id: str = None):
        self.name = name
        self.business_type = business_type
        self.property_id = property_id
        self.required_structures = required_structures
        self.workforce = workforce

    @staticmethod
    def from_dict(source):
        business = Business(name=source['name'], business_type=source['business_type'],
                            required_structures=source['required_structures'], workforce=source['workforce'])
        if 'property_id' in source:
            business.property_id = source['property_id']
        return business

    def production_preparing(self, prop, storage: Storage) -> bool:
        required_structures = self.required_structures
        structure_id = "_none" if prop.structure_id is None else prop.structure_id
        if structure_id in required_structures:
            self.workforce['_reserved_bonus'] = required_structures[structure_id]['bonus']
            return True
        else:
            return False

    def run(self, prop, storage: Storage):
        if 'production_t_plus' in self.workforce:
            self.workforce['production_t_plus'] -= 1

        success = self.production_preparing(prop=prop, storage=storage)

        if success and '_reserved_workforce' in self.workforce:
            workforce_earned = self.workforce['_reserved_workforce']
            if '_reserved_bonus' in self.workforce:
                workforce_earned = workforce_earned * self.workforce['_reserved_bonus']
            self.workforce['amount'] += int(workforce_earned)
            if self.workforce['amount'] >= 0:
                if 'production_t_plus' not in self.workforce or self.workforce['production_t_plus'] <= 0:
                    debug_toolkit.debug_print('Business Run', 'Production Complete')
                    # complete
        elif success:
            debug_toolkit.warning_print('Business Run', '_reserved_workforce not specify', [self.workforce.__str__()])
        self.workforce['_reserved_workforce'] = 0

