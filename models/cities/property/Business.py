class Business(object):
    def __init__(self, name: str, property_id: str, required_structure_id: str,
                 bonus_package: dict,
                 experience_acquire: list[str],
                 experience_acquire_chance: list[float],
                 workforce: dict,
                 workforce_bonus: dict,):
        self.name = name
        self.property_id = property_id
        self.required_structure_id = required_structure_id
        self.bonus_package = bonus_package
        self.experience_acquire = experience_acquire
        self.experience_acquire_chance = experience_acquire_chance
        self.workforce = workforce
        self.workforce_bonus = workforce_bonus
