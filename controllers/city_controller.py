from models.GameData import GameData
from models.Human import Human
from models.Storage import Storage
from models.cities.City import City
from controllers.random_controller import check_random_result
from controllers.market_controller import purchase
from controllers.property_controller import g_new_property


def cities_loop(game_data: GameData):
    for _, city in game_data.cities.items():
        city_loop(game_data=game_data, city=city)


def city_loop(game_data: GameData, city: City):
    population_loop(game_data=game_data, city=city)
    if city.population.size(employed=False) > 2:
        g_new_property(game_data=game_data, city=city)


def population_loop(game_data: GameData, city: City):
    products_needed = Storage()
    budget = 0
    born_count = 0
    for human in city.population.humans:
        products_needed.combine(game_data.environment.human_needs[human.level])
        if human.property_id is not None:
            budget += human.salary
        else:
            budget += int(human.salary * 0.5)
    purchased_storage = Storage()
    purchased_storage.products = purchase(game_data=game_data, buyer_fe_id=city.financial_id,
                                          products=products_needed.products, city=city, budget=budget)
    human_feed(game_data=game_data, human_list=city.population.humans, products=purchased_storage)
    dead_list = []
    for human in city.population.humans:
        human_breed(human=human)
        if human_starving(human=human):
            dead_list.append(human)
    if len(dead_list) > 0:
        for dead_human in dead_list:
            city.population.humans.remove(dead_human)
    if born_count > 0:
        while born_count > 0:
            born_count -= 1
            b_new_human(city=city)


def human_feed(game_data: GameData, human_list: list[Human], products: Storage):
    human_needs = game_data.environment.human_needs
    for human in human_list:
        if products.remove(human_needs[human.level]):
            human_satisfy(human=human, completely=True)
        else:
            for product_id, amount in human_needs[human.level]:
                product = game_data.products[product_id]
                if product.category == 0 and products.remove_as_much_as_possible(product_id, amount) == amount:
                    human_satisfy(human=human, completely=False)
                    continue
            human_not_satisfy(human=human)


def human_satisfy(human: Human, completely: bool):
    if 'wohaole' in human.buffs:
        if human.buffs['wohaole'] < 1.0:
            if completely:
                human.buffs['wohaole'] += 0.01
            else:
                human.buffs['wohaole'] += 0.02
    if 'woele' in human.buffs:
        if human.buffs['woele'] > 0.0:
            if completely:
                human.buffs['woele'] -= 0.10
            else:
                human.buffs['woele'] -= 0.05


def human_not_satisfy(human: Human):
    if 'wohaole' in human.buffs:
        if human.buffs['wohaole'] > 0.0:
            human.buffs['wohaole'] -= 0.1
    if 'woele' in human.buffs:
        if human.buffs['woele'] < 1.0:
            human.buffs['woele'] += 0.10


def human_breed(human: Human) -> bool:
    if 'wohaole' in human.buffs:
        if check_random_result(human.buffs['wohaole']):
            human.buffs['wohaole'] = 0.0
            return True
    return False


def human_starving(human: Human) -> bool:
    if 'woele' in human.buffs:
        if check_random_result(human.buffs['woele']):
            return True
    return False


def b_new_human(city: City):
    human = Human(level=0)
    city.population.humans.append(human)


def get_city(game_data: GameData, city_id: str):
    return game_data.cities[city_id]
