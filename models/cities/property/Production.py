from models.cities.personality.PersonalityExperience import PersonalityExperience


class Production(object):
    def __init__(self, name: str, products: dict, designo_multiplier: int, software_solution_multiplier: int,
                 experience_required: list[PersonalityExperience], experience_acquire: list[PersonalityExperience],
                 experience_acquire_chance: list[float], required_structure: ,
                 work_force: int, duration: int, number_of_min_employees: int, number_of_max_employees: int,
                 consumes: dict = None, designo_id: str = None, software_solution_id: str = None):
        self.name = name
        self.consumes = consumes
        self.products = products
        self.designo_id = designo_id
        self.designo_multiplier = designo_multiplier
        self.software_solution_id = software_solution_id
        self.software_solution_multiplier = software_solution_multiplier
        self.experience_required = experience_required
        self.experience_acquire = experience_acquire
        self.experience_acquire_chance = experience_acquire_chance
        self.required_structure =
        self.work_force = work_force
        self.duration = duration
        self.number_of_min_employees = number_of_min_employees
        self.number_of_max_employees = number_of_max_employees
        self.buffs = dict()
