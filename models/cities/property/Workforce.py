from models.cities.personality.PersonalityExperience import PersonalityExperience


class Workforce(object):
    def __init__(self, producer_id: str, personality_experience_list: list[PersonalityExperience], expiry_t_plus: int):
        self.producer_id = producer_id
        self.experience_list = personality_experience_list
        self.expiry_t_plus = expiry_t_plus
