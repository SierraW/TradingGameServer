from models.cities.personality.PersonalityExperience import PersonalityExperience
from models.cities.property.BonusPackage import BonusPackage


class Production(object):
    def __init__(self, name: str, product_amount: dict,
                 experience_acquire: list[str],
                 experience_acquire_chance: list[float],
                 workforce: dict,
                 workforce_bonus: dict,
                 production_t_plus: int,
                 required_structures: list,
                 bonus_package: BonusPackage = None,
                 base_charming: int = None,
                 consume_amount: dict = None,
                 consume_charming_filter: dict = None,
                 storage_in_id: str = None,
                 storage_out_id: str = None,
                 buffs: dict = None,):
        self.name = name
        self.consume_amount = consume_amount
        self.consume_charming_filter = consume_charming_filter
        self.product_amount = product_amount
        self.base_charming = base_charming
        self.experience_acquire = experience_acquire
        self.experience_acquire_chance = experience_acquire_chance
        self.required_structures = required_structures
        self.workforce = workforce
        self.production_t_plus = production_t_plus
        self.workforce_bonus = workforce_bonus

        self.storage_in_id = storage_in_id
        self.storage_out_id = storage_out_id

        self.bonus_package = bonus_package
        if buffs is None:
            self.buffs = dict()

    @staticmethod
    def from_dict(source):
        production = Production(name=source['name'], product_amount=source['product_amount'],
                                experience_acquire=source['experience_acquire'],
                                experience_acquire_chance=source['experience_acquire_chance'],
                                required_structures=source['required_structures'],
                                workforce=source['workforce'],
                                production_t_plus=source['production_t_plus'],
                                workforce_bonus=source['workforce_bonus'])
        if 'bonus_package' in source:
            production.bonus_package = BonusPackage.from_dict(source['bonus_package'])
        if 'base_charming' in source:
            production.base_charming = source['base_charming']
        if 'base_charming' in source:
            production.base_charming = source['base_charming']
        if 'required_structure_id' in source:
            production.required_structure_id = source['required_structure_id']
        if 'consume_amount' in source:
            production.consume_amount = source['consume_amount']
            if 'consume_charming_filter' in source:
                production.consume_charming_filter = source['consume_charming_filter']
        if 'storage_in_id' in source:
            production.storage_in_id = source['storage_in_id']
        if 'storage_out_id' in source:
            production.storage_out_id = source['storage_out_id']
        return production
