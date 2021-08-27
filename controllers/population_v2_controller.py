import copy

import debug_toolkit
from controllers.algorithm_club import random_check, random_range, random_choice
from controllers.financial_controller import register_financial_entity, transfer_all
from .work_contract_controller import work_contract_accept_offer
from models.GameData import GameData
from models.cities.City import City
from models.cities.personality.Family import Family
from models.cities.personality.Human import Human


def population_loop(game_data: GameData):
    count = 0
    for human_id, human in game_data.humans.items():
        if human.family_id is None and human.prefer_purchase_weekday == game_data.environment.time.weekday:
            count += 1
    for family_id, family in game_data.families.items():
        count += 1
    debug_toolkit.debug_print('population_loop', 'count', [count])


def population_loop_single(human_id: str, human: Human):
    pass


def population_get_resume(game_data: GameData):
    pass


def population_accept_resume(game_data: GameData, human_id: str, human: Human):
    career_offers = game_data.career_fair[human_id]
    career_offer = random_choice(career_offers)
    work_contract_accept_offer(game_data=game_data, offer=career_offer, human_id=human_id)


def population_post_resume(game_data: GameData, human_id: str):
    game_data.career_fair[human_id] = []


def population_marriage(game_data: GameData, family_last_name: str, human_id_a: str, human_id_b: str) -> str:
    family_fe_id = register_financial_entity(game_data=game_data, name=f'{family_last_name}\'s Family', entity_type=6)
    human_a = game_data.humans[human_id_a]
    human_a.family_id = family_fe_id
    human_b = game_data.humans[human_id_b]
    human_b.family_id = family_fe_id
    transfer_all(game_data=game_data, sender_fe_id=human_a.financial_entity_id, receiver_fe_id=family_fe_id)
    transfer_all(game_data=game_data, sender_fe_id=human_b.financial_entity_id, receiver_fe_id=family_fe_id)
    family = Family(family_last_name=family_last_name, family_member_id_list=[human_id_a, human_id_b],
                    financial_entity_id=family_fe_id)
    game_data.families[family_fe_id] = family
    return family_fe_id


def population_family_add_to_family(game_data: GameData, family_id: str, new_member_id: str):
    family = game_data.families[family_id]
    new_member = game_data.humans[new_member_id]
    new_member.family_id = family_id
    transfer_all(game_data=game_data, sender_fe_id=new_member.financial_entity_id,
                 receiver_fe_id=family.financial_entity_id)
    family.family_member_id_list.append(new_member_id)


def population_init_human(game_data: GameData, city_id: str, city: City):
    if 'age_distribution' in city.population:
        first_name_pool = city.population['first_name_pool']
        last_name_pool = city.population['last_name_pool']

        def become_human() -> list[str]:
            return [random_choice(first_name_pool), random_choice(last_name_pool)]

        experience_chance_dict = city.population['experience_chance_dict']

        def get_experience_list(human_input: Human):
            for experience_id, chance_list in experience_chance_dict.items():
                if human_input.age < chance_list[0]:
                    continue
                if random_check(chance_list[1]):
                    experience = copy.deepcopy(game_data.experiences[experience_id])
                    experience.formation_time = 0
                    human_input.personality_experience_list.append(experience)
                    debug_toolkit.debug_print('successfully create skill', args=[experience, human_input])

        total_population = 0
        age_distribution_list = city.population['age_distribution']
        for age_distribution in age_distribution_list:
            range_of_age = age_distribution[0]
            population = age_distribution[1]
            rate_of_family = age_distribution[2]
            range_of_saving = age_distribution[3]
            while population > 0:
                age = random_range(range_list=range_of_age)
                saving = random_range(range_of_saving)
                male = random_check(0.5)
                name = become_human()
                prefer_purchase_weekday = random_range([0, 6])
                human = Human(first_name=name[0], last_name=name[1], age=age,
                              financial_entity_id=register_financial_entity(game_data=game_data,
                                                                            name=f'{name[0]} {name[1]}',
                                                                            entity_type=0, currency_dict={
                                      city.currency_id: saving
                                  }),
                              gender_male=male, city_id=city_id,
                              personality_experience_list=[],
                              personality_network=[],
                              prefer_purchase_weekday=prefer_purchase_weekday)
                get_experience_list(human_input=human)
                human_id = game_data.generate_identifier()
                game_data.humans[human_id] = human
                population -= 1
                if random_check(rate_of_family):
                    age = random_range(range_list=range_of_age)
                    name_1 = become_human()
                    human = Human(first_name=name_1[0], last_name=name_1[1], age=age,
                                  financial_entity_id=register_financial_entity(game_data=game_data,
                                                                                name=f'{name_1[0]} {name_1[1]}',
                                                                                entity_type=0),
                                  gender_male=not male, city_id=city_id,
                                  personality_experience_list=[], personality_network=[],
                                  prefer_purchase_weekday=prefer_purchase_weekday)
                    get_experience_list(human_input=human)
                    human_id_1 = game_data.generate_identifier()
                    game_data.humans[human_id_1] = human
                    population -= 1
                    family_id = population_marriage(family_last_name=name_1[1], game_data=game_data,
                                                    human_id_a=human_id, human_id_b=human_id_1)
                    if len(age_distribution) == 6:
                        child_age_range_list = age_distribution[4]
                        range_of_extra_per_kid = age_distribution[5]
                        for child_age_range_chance_list in child_age_range_list:
                            child_age_range = child_age_range_chance_list[0]
                            child_chance = child_age_range_chance_list[1]
                            addition_fund = random_range(range_of_extra_per_kid)
                            if random_check(child_chance):
                                name = become_human()
                                male = random_check(0.5)
                                child_age = random_range(child_age_range)
                                child = Human(first_name=name[0], last_name=name_1[1], age=child_age,
                                              financial_entity_id=register_financial_entity(game_data=game_data,
                                                                                            name=f'{name_1[0]} '
                                                                                                 f'{name_1[1]}',
                                                                                            entity_type=0,
                                                                                            currency_dict={
                                                                                                city.currency_id:
                                                                                                    addition_fund
                                                                                            }),
                                              gender_male=male, city_id=city_id,
                                              personality_experience_list=[], personality_network=[],
                                              prefer_purchase_weekday=prefer_purchase_weekday)
                                get_experience_list(child)
                                child_id = game_data.generate_identifier()
                                game_data.humans[child_id] = child
                                population_family_add_to_family(game_data=game_data, family_id=family_id,
                                                                new_member_id=child_id)
            total_population += age_distribution[1]
        return total_population
