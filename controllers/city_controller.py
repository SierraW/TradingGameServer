from controllers.population_controller import population_loop
from models.GameData import GameData
from models.cities.City import City
from controllers.property_controller import g_new_property, get_properties_by_city, register_property_for_sale, \
    get_property_listings
from controllers.company_controller import register_company, calculate_minimum_budget_for_a_year
from controllers.financial_controller import count


def cities_loop(game_data: GameData):
    for city_id, city in game_data.cities.items():
        city_loop(game_data=game_data, city_id=city_id, city=city)


def city_loop(game_data: GameData, city_id: str, city: City):
    population_loop(game_data=game_data, city=city)
    population_size = city.population.size()
    property_dict = get_properties_by_city(game_data=game_data, city_id=city_id)
    if city.population.size(employed=False) > 2:
        prop_id = g_new_property(game_data=game_data, city=city)
        price = 0
        register_property_for_sale(game_data=game_data, prop_id=prop_id, seller_fe_id=city.financial_id, price=price,
                                   currency_id=city.currency_id)
    property_listings = get_property_listings(game_data=game_data, city_id=city_id)
    if len(property_listings) > 0:
        budget = count(game_data=game_data, fe_id=city.financial_id, currency_id=city.currency_id)
        minimum_budget = calculate_minimum_budget_for_a_year(game_data=game_data, city=city) * 5
        if budget > minimum_budget:
            register_company(game_data=game_data, name=f'{city.name} 国有公司', initial_stock_distribution={
                city.financial_id: 10000
            }, fund_distribution={
                city.financial_id: minimum_budget
            }, city_id=city_id, auto_managed=True)



def get_city(game_data: GameData, city_id: str):
    return game_data.cities[city_id]
