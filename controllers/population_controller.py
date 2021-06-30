from data import GameData
from models.Human import Human
from models.cities.City import City
from models.cities.Population import Population
from models.cities.property.Property import Property
from controllers.financial_controller import transfer


def get_unemployed_human(population: Population, level: int = None) -> list:
    unemployed_list = filter(lambda human: human.property_id is None, population.humans)
    if level is not None:
        return list(filter(lambda human: human.level == level, unemployed_list))
    return list(unemployed_list)


def get_employer_salary(population: Population, level: int = None) -> float:
    return population.salaries[level]


def employ(game_data: GameData, city: City, human: Human, currency_id: str, salary: int, prop_id: str,
           prop: Property, duration: int) -> bool:
    human.property_id = prop_id
    if transfer(game_data=game_data, sender_fe_id=prop.financial_id, receiver_fe_id=city.financial_id,
                currency_id=currency_id, amount=salary):
        human.property_id = prop_id
        human.contract_remaining_days = duration
        return True
    return False


def get_employees(population: Population, prop_id: str) -> list:
    return list(filter(lambda human: human.property_id == prop_id, population.humans))
