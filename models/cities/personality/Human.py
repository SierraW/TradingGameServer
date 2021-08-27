from models.Wallet import Wallet
from models.cities.personality.PersonalityExperience import PersonalityExperience
from models.cities.personality.PersonalityWorkContract import PersonalityWorkContract


class Human(object):
    def __init__(self, first_name: str, last_name: str, age: int, financial_entity_id: str,
                 gender_male: bool, city_id: str,
                 personality_experience_list: list[PersonalityExperience],
                 personality_network: list[str],
                 prefer_purchase_weekday: int,
                 family_id: str = None,
                 personality_work_contracts: list[str] = None, buffs: dict = None):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.family_id = family_id
        self.financial_entity_id = financial_entity_id
        self.gender_male = gender_male
        self.city_id = city_id
        self.personality_experience_list = personality_experience_list
        self.personality_network = personality_network
        self.prefer_purchase_weekday = prefer_purchase_weekday
        self.prefer_day = 364
        self.prefer_day_leap_year = 365
        self.prefer_year_remainder = 20
        if buffs is None:
            self.buffs = dict()
        else:
            self.buffs = buffs
        if personality_work_contracts is None:
            self.personality_work_contracts = []
        else:
            self.personality_work_contracts = personality_work_contracts
