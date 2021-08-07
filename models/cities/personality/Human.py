from models.Wallet import Wallet
from models.cities.personality.PersonalityExperienceSet import PersonalityExperienceSet
from models.cities.personality.PersonalityWorkContract import PersonalityWorkContract


class Human(object):
    def __init__(self, age: int, personality_experience_set: PersonalityExperienceSet, personality_network: list[int],
                 personality_work_contract: PersonalityWorkContract, buffs: dict):
        self.age = age
        self.personality_experience_set = personality_experience_set
        self.personality_network = personality_network
        self.buffs = buffs
        self.personality_work_contract = personality_work_contract
