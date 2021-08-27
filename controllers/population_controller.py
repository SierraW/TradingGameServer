import copy
import random

from controllers.market_controller import market_purchase_by_category, market_purchase
from controllers.random_controller import check_random_result
from data import GameData
from models.cities.personality.Human import Human
from models.cities.City import City
from models.cities.personality.PersonalityOffer import PersonalityOffer
from models.cities.personality.Population import Population
from models.cities.property.Property import Property
from controllers.financial_controller import transfer, financial_count, get_population_fe_id


def population_loop(game_data: GameData, city: City):
    budget = financial_count(game_data=game_data, fe_id=city.financial_id, currency_id=city.currency_id)
    food_bank = market_purchase_by_category(game_data=game_data, buyer_fe_id=city.financial_id, category=0,
                                            amount_required=len(city.population.humans), market_id=city.market_id,
                                            available_budget=budget, destination_storage_id=city.population.storage_id)
    human_dead(population=city.population, food_supply_amount=food_bank.amount)
    human_needs = copy.deepcopy(game_data.environment.human_needs)
    breed_count = 0
    for human in city.population.humans:
        breed_count += 1 if human_breed(human=human) else 0
        if human.property_id is None:
            get_a_job(game_data=game_data, human=human, city=city)
        else:
            brought = market_purchase(game_data=game_data, buyer_fe_id=city.population.fe_accounts[human.level],
                                      products=human_needs[human.level], market_id=city.market_id,
                                      destination_storage_id=city.population.storage_id,
                                      budget=int(get_employee_salary(population=city.population, level=human.level)))
            human_satisfy(human=human, products=brought, required=human_needs[human.level])
    for _ in range(breed_count % 10):
        b_new_human(city=city)


def human_satisfy(human: Human, products: dict, required: dict):
    popu_max = 0
    count = 0
    for pid, amount in required.items():
        if pid in products:
            if amount <= products[pid]:
                popu_max += amount
                count += amount
            else:
                popu_max += amount
                count += products[pid]
        else:
            popu_max += amount
    if 'buff_human_satisfaction' in human.buffs:
        if popu_max - count == 0:
            if human.buffs['buff_human_satisfaction'] < 0.99:
                human.buffs['buff_human_satisfaction'] += 0.01
        else:
            if human.buffs['buff_human_satisfaction'] < 0.1:
                human.buffs['buff_human_satisfaction'] = 0
            else:
                human.buffs['buff_human_satisfaction'] -= 0.01 * (popu_max - count) if popu_max - count < 10 else 10
        if check_random_result(human.buffs['buff_human_satisfaction']):
            human.buffs['buff_human_satisfaction'] = 0.0
            if human.level < 3:
                human.level += 1
                human.buffs['buff_human_satisfaction'] = 0


def human_breed(human: Human) -> bool:
    if 'wohaole' in human.buffs:
        if check_random_result(human.buffs['wohaole']):
            human.buffs['wohaole'] = 0.0
            return True
    return False


def human_dead(population: Population, food_supply_amount: int):
    starving_amount = len(population.humans) - food_supply_amount
    print(f'starving!! {starving_amount}')
    while starving_amount > 0 and len(population.humans) > 2:
        starving_amount -= 1
        human = priority_human(humans=population.humans)
        if 'woele' in human.buffs:
            if human.buffs['woele'] < 1.0:
                human.buffs['woele'] += 0.10
        if 'wohaole' in human.buffs:
            if human.buffs['wohaole'] > 0.5:
                human.buffs['wohaole'] -= 0.5
            else:
                human.buffs['wohaole'] = 0.0
        if 'woele' in human.buffs:
            if check_random_result(human.buffs['woele']):
                population.humans.remove(human)
    if starving_amount == 0:
        for human in population.humans:
            if 'woele' in human.buffs:
                human.buffs['woele'] = 0.0
            if 'wohaole' in human.buffs:
                if human.buffs['wohaole'] < 0.99:
                    human.buffs['wohaole'] += 0.01


def priority_human(humans: list[Human]):
    if len(humans) == 0:
        print('PopulationController priority_human: No humans available for selecting.')
        return
    list_of_humans_awaiting = list(filter(lambda temp_human: temp_human.property_id is None, humans))
    if len(list_of_humans_awaiting) == 0:
        list_of_humans_awaiting = humans
    selected_humans = []
    minimum_level = 4
    minimum_level_human_index = 0
    for i in range(10):
        human = random.choice(list_of_humans_awaiting)
        if human.level == 0:
            return human
        if human.level < minimum_level:
            minimum_level = human.level
            minimum_level_human_index = i
        selected_humans.append(human)
    return selected_humans[minimum_level_human_index]


def b_new_human(city: City):
    human = Human(level=0)
    city.population.humans.append(human)


def get_unemployed_human(population: Population, level: int = None) -> list:
    unemployed_list = filter(lambda human: human.property_id is None, population.humans)
    if level is not None:
        return list(filter(lambda human: human.level == level, unemployed_list))
    return list(unemployed_list)


def get_employee_salary(population: Population, level: int = None) -> float:
    if level is None:
        total_salary = 0
        for salary in population.salaries:
            total_salary += salary
        return int(total_salary / len(population.humans))
    return population.salaries[level]


def get_a_job(game_data: GameData, human: Human, city: City):
    desired_level = human.level
    offers = []
    while len(offers) == 0 and desired_level >= 0:
        offers = find_offer_by_level(level=desired_level, population=city.population)
        desired_level -= 1
    if len(offers) > 0:
        offer = sorted(offers, key=lambda human_offer: human_offer.one_time_payment, reverse=True)[0]
        accept_offer(game_data=game_data, city=city, human=human, offer=offer)


def accept_offer(game_data: GameData, city: City, human: Human, offer: PersonalityOffer):
    if offer.one_time_payment > 0:
        if not transfer(game_data=game_data, sender_fe_id=offer.company_id,
                        receiver_fe_id=get_population_fe_id(population=city.population, level=human.level),
                        currency_id=city.currency_id,
                        amount=offer.one_time_payment):
            return
    human.property_id = offer.property_id
    city.population.offers.remove(offer)


def find_offer_by_level(level: int, population: Population) -> list[PersonalityOffer]:
    return list(filter(lambda offer: offer.level == level, population.offers))


def remove_all_previous_offer_by_property_id(city: City, property_id: str):
    city.population.offers = list(filter(lambda offer: offer.property_id == property_id, city.population.offers))


def send_offer(company_id: str, city: City, property_id: str, level: int, amount: int,
               payment_per_employee: int = None, budget_per_employee: int = None) -> bool:
    if payment_per_employee is None:
        offers = sorted(find_offer_by_level(level=level, population=city.population), reverse=True,
                        key=lambda offer: offer.one_time_payment)
        highest_price = 0
        if len(offers) > 0:
            highest_price = offers[0].one_time_payment
        highest_price = int(highest_price * 1.05)
        if budget_per_employee is not None and highest_price > budget_per_employee:
            return False
        payment_per_employee = highest_price
    for _ in range(amount):
        city.population.offers.append(HumanOffer(company_id=company_id, property_id=property_id, level=level,
                                                 one_time_payment=payment_per_employee))
    return True


def employ(game_data: GameData, city: City, human: Human, currency_id: str, salary: int, prop_id: str,
           prop: Property, duration: int) -> bool:
    human.property_id = prop_id
    if transfer(game_data=game_data, sender_fe_id=prop.financial_id, receiver_fe_id=city.financial_id,
                currency_id=currency_id, amount=salary):
        human.property_id = prop_id
        human.contract_remaining_days = duration
        return True
    return False


def unemployed(human: Human):
    human.property_id = None
    human.contract_remaining_days = None


def unemployed_all_employees_except(level: int, employees: list[Human]) -> list[Human]:
    remaining_employees = []
    for employee in employees:
        if employee.level == level:
            remaining_employees.append(employee)
        else:
            unemployed(human=employee)
    return remaining_employees


def get_employees(population: Population, prop_id: str) -> list:
    return list(filter(lambda human: human.property_id == prop_id, population.humans))
