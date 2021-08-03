from controllers.population_controller import population_loop
from models.GameData import GameData
from models.cities.City import City
from controllers.property_controller import property_generate_property, get_properties_by_city, \
    property_register_property_for_sale, get_property_listings
from controllers.company_controller import company_register_company, company_calculate_minimum_budget_for_a_year
from controllers.financial_controller import financial_count


def city_get_city(game_data: GameData, city_id: str) -> City:
    city = game_data.cities[city_id]
    city.city_id = city_id
    return city


def cities_loop(game_data: GameData):
    for city_id, city in game_data.cities.items():
        city_loop(game_data=game_data, city_id=city_id, city=city)


def city_loop(game_data: GameData, city_id: str, city: City):
    population_loop(game_data=game_data, city=city)
    population_size = city.population.size()
    property_dict = get_properties_by_city(game_data=game_data, city_id=city_id)
    if city.population.size(employed=False) > 2:
        prop_id = property_generate_property(game_data=game_data, city_id=city_id, city=city)
        price = 0
        property_register_property_for_sale(game_data=game_data, prop_id=prop_id, seller_fe_id=city.financial_id, price=price,
                                            currency_id=city.currency_id)
    property_listings = get_property_listings(game_data=game_data, city_id=city_id)

