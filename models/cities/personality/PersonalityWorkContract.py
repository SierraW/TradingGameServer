class PersonalityWorkContract(object):
    def __init__(self, start_t_plus: int, end_t_plus: int, property_id: str, work_day: list[int]):
        self.start_t_plus = start_t_plus
        self.end_t_plus = end_t_plus
        self.property_id = property_id
        self.work_day = work_day
