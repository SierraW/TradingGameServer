from controllers.storage_controller import *
from models.GameData import GameData
from models.Company import Company
from models.Human import Human
from models.cities.City import City
from models.cities.property.Property import Property
from controllers.market_controller import register_market_listing
from controllers.financial_controller import transfer
from controllers.population_controller import get_unemployed_human, employ, get_employees


def properties_loop(game_data: GameData):
    for prop_id, item in game_data.properties.items():
        property_loop(game_data=game_data, prop_id=prop_id, prop=item)


def property_loop(game_data: GameData, prop_id: str, prop: Property, company: Company):
    city = game_data.cities[prop.city_id]
    employee_list = get_employees(population=city.population, prop_id=prop_id)
    # assign prop size
    size = len(employee_list)
    if size >= 10:
        size = 3
    elif size >= 9:
        size = 2
    elif size >= 3:
        size = 1
    else:
        size = 0
    production_loop(game_data=game_data, prop=prop, prop_size=size)
    if prop.auto_management:

        auto_management(game_data=game_data, company=company,
                        prop_size=size, employees=employee_list, city=city, prop_id=prop_id, prop=prop)


def auto_management(game_data: GameData, company: Company, prop_size: int, employees: list[Human], city: City,
                    prop_id: str, prop: Property):
    if company.budget_cap <= 0:
        return
    if prop_size < 3:
        unemployment_list = get_unemployed_human(population=city.population, level=prop.production.level)
        if len(unemployment_list) > 0:
            unemployment_list = sorted(unemployment_list, key=lambda human: human.salary)
            offered = unemployment_list[0]
            if offered.salary <= company.budget_cap:
                employ(game_data=game_data, city=city, human=offered, currency_id=city.currency_id,
                       salary=offered.salary, prop_id=prop_id, prop=prop)
                company.budget_cap -= offered.salary






def g_new_property(game_data: GameData, city: City):
    prop_id = game_data.generate_identifier()
    city.property_counter += 1
    game_data.properties[prop_id] = Property(city_id=city.city_id, name=f'No.{city.property_counter}',
                                             financial_id=city.financial_id)


def production_loop(game_data: GameData, prop: Property, prop_size: int):
    if prop.production.num_of_days_remaining is not None:
        if prop.production.num_of_days_remaining > 0:
            prop.production.num_of_days_remaining -= 1
            return
        else:
            prop.production.num_of_days_remaining = None
            _end_production(game_data, prop, prop_size=prop_size)
    _start_production(game_data, prop, prop_size=prop_size)


def _start_procedure(game_data: GameData, prop: Property, prop_size: int) -> bool:
    if 'womole' in prop.buffs:
        if game_data.environment.time.season == 1 or game_data.environment.time.season == 3:
            return False
    if prop.production.consumes is not None:
        if not remove_from_storage(game_data, prop.production.get_consumes(prop_size), prop.storage_in_id):
            return False
    return True


def _start_production(game_data: GameData, prop: Property, prop_size: int):
    if not _start_procedure(game_data, prop, prop_size=prop_size):
        return
    prop.production.start_production()


def _end_production(game_data: GameData, prop: Property, prop_size: int):
    end_multiplier = prop.production.get_multiplier(prop_size)
    if 'woliele' in prop.production.buffs:
        buff = game_data.buffs['woliele']
        end_multiplier *= buff.key_effect_data[0]
    if 'wobaole' in prop.buffs:
        buff = game_data.buffs['wobaole']
        end_multiplier *= buff.key_effect_data[0]
    end_products = {k: int(v * end_multiplier) for k, v in prop.production.products.items()}
    if prop.storage_out_id is None:
        market_id = prop.auto_register_market_id
        if market_id is None:
            market_id = game_data.cities[prop.city_id].market_id
        for product_id, amount in end_products.items():
            register_market_listing(game_data=game_data, market_id=market_id, seller_fe_id=prop.financial_id, product_id=product_id,
                                    amount=amount)
    else:
        add_to_storage(game_data, end_products, prop.storage_out_id)


def get_properties(game_data: GameData, company: Company) -> dict:
    fetch_result = dict()
    for prop_id, prop in game_data.properties:
        if prop.financial_id == company.financial_id:
            fetch_result[prop_id] = prop
    return fetch_result


def get_property_listings(game_data: GameData, city_id: str) -> dict:
    fetch_result = dict()
    for pl_id, pl in game_data.property_listings.items():
        if pl.city_id == city_id:
            fetch_result[pl_id] = pl
    return fetch_result


def purchase_property(game_data: GameData, prop_listing_id: str, buyer_fe_id: str) -> bool:
    prop_listing = game_data.property_listings[prop_listing_id]
    prop = game_data.properties[prop_listing.property_id]
    if prop_listing is None:
        return False
    if prop_listing.target_buyer_fe_id is not None and prop_listing.target_buyer_fe_id != buyer_fe_id:
        return False
    if transfer(game_data=game_data, sender_fe_id=buyer_fe_id, receiver_fe_id=prop.financial_id,
                currency_id=prop_listing.currency_id, amount=prop_listing.price):
        prop.financial_id = buyer_fe_id
        prop.auto_management = True
        return True
    return False

