from controllers.algorithm_club import find_most_common_level, find_desired_employee_amount
from controllers.financial_controller import transfer, financial_count
from controllers.market_controller import market_get_recommended_pricing, get_previous_average_price, \
    market_get_lowest_listing_price_for_product, market_register_product
from controllers.population_controller import get_employees, get_employee_salary, \
    unemployed_all_employees_except, remove_all_previous_offer_by_property_id, send_offer, unemployed
from controllers.storage_controller import *
from models.cities.company.Company import Company
from models.GameData import GameData
from models.cities.personality.Human import Human
from models.PropertyListing import PropertyListing
from models.cities.City import City
from models.cities.property.Production import Production
from models.cities.property.Property import Property


def property_get_property(game_data: GameData, prop_id: str) -> Property:
    return game_data.properties[prop_id]


def properties_loop(game_data: GameData):
    for prop_id, prop in game_data.properties.items():
        if prop.financial_id in game_data.companies:
            property_loop(game_data=game_data, prop_id=prop_id, prop=prop,
                          company=game_data.companies[prop.financial_id])


def property_size(employee_list: list[Human], production_level: int) -> int:
    contains_level_3_worker = False
    size = 0
    for human in employee_list:
        if human.level >= production_level:
            size += 1
        if human.level == 3:
            contains_level_3_worker = True
    if size >= 9:
        size = 2
    elif size >= 3:
        size = 1
    else:
        size = 0
    if contains_level_3_worker:
        size += 1
    return size


def property_loop(game_data: GameData, prop_id: str, prop: Property, company: Company):
    city = game_data.cities[prop.city_id]
    employee_list = get_employees(population=city.population, prop_id=prop_id)
    # assign prop size
    if prop.production is not None:
        size = property_size(employee_list=employee_list,
                             production_level=prop.production.level if prop.production is not None else 0)
        production_loop(game_data=game_data, prop=prop, prop_size=size)
    if prop.auto_managed:
        auto_management(game_data=game_data, company=company, employees=employee_list, city=city, prop_id=prop_id,
                        prop=prop)


def auto_management(game_data: GameData, company: Company, employees: list[Human], city: City,
                    prop_id: str, prop: Property):
    if prop.production is None:
        _auto_management_choose_production_and_manage_human_resources(game_data, company, employees, city,
                                                                      prop_id, prop)


def _auto_management_choose_production_and_manage_human_resources(game_data: GameData, company: Company,
                                                                  employees: list[Human], city: City,
                                                                  prop_id: str, prop: Property, repeated: bool = False):
    preferred_level = find_most_common_level(humans=employees) if len(employees) > 0 else 0
    employees = unemployed_all_employees_except(level=preferred_level, employees=employees)
    preferred_prop_size = find_desired_employee_amount(num_of_employee=len(employees))
    preferred_prop_size_level = 1 if preferred_prop_size < 4 else 2
    productions_choose = list(filter(lambda temp_production: temp_production.level == preferred_level,
                                     city.productions))
    most_profitable_production = None
    max_approx_profit = 0
    for production in productions_choose:
        city = game_data.cities[prop.city_id]
        income = get_estimated_income_per_year(game_data=game_data, city=city, production=production,
                                               targeted_level=preferred_prop_size_level)
        cost = get_estimated_cost_per_year(game_data=game_data, city=city, production=production,
                                           targeted_level=preferred_prop_size_level)
        if financial_count(game_data=game_data, fe_id=prop.financial_id, currency_id=city.currency_id) > int(
                cost * 0.5):
            if income is None:
                most_profitable_production = production
                break
            profit = income - cost
            if most_profitable_production is None or profit > max_approx_profit:
                most_profitable_production = production
                max_approx_profit = profit
    if most_profitable_production is None:
        if not repeated:
            _auto_management_choose_production_and_manage_human_resources(game_data, company, employees, city, prop_id,
                                                                          prop, True)
        return
    else:
        assign_production_task(prop=prop, production=most_profitable_production)
    if len(employees) < preferred_prop_size:
        remove_all_previous_offer_by_property_id(city=city, property_id=prop_id)
        send_offer(company_id=company.financial_id, city=city, property_id=prop_id, level=preferred_level,
                   amount=preferred_prop_size - len(employees))
    else:
        while len(employees) > preferred_prop_size:
            unemployed(human=employees[0])
            del employees[0]


def get_estimated_cost_per_year(game_data: GameData, city: City, production: Production,
                                targeted_level: int = 1) -> int:
    targeted_num_of_employees = 1
    cost = 0
    if targeted_level == 1:
        targeted_num_of_employees = 3
    elif targeted_level == 2:
        targeted_num_of_employees = 9
    elif targeted_level > 2:
        cost += get_employee_salary(population=city.population, level=3) * 120
        targeted_num_of_employees = 8
    employee_single_cost = get_employee_salary(population=city.population, level=production.level)
    cost += employee_single_cost * targeted_num_of_employees * 120
    num_of_productions_made = 120 / production.duration
    for consume, value in production.get_consumes(level=targeted_level).items():
        price = get_previous_average_price(game_data=game_data, market_id=city.market_id, product_id=consume,
                                           currency_id=city.currency_id)
        cost += int(price * value * num_of_productions_made)
    return cost


def get_estimated_income_per_year(game_data: GameData, city: City, production: Production,
                                  targeted_level: int = 1):
    income = 0
    num_of_productions_made = 120 / production.duration
    for product, value in get_end_products_after_multiplier(game_data=game_data, production=production,
                                                            prop_size=targeted_level).items():
        price = get_previous_average_price(game_data=game_data, market_id=city.market_id, product_id=product,
                                           currency_id=city.currency_id)
        if price is None:
            price = market_get_lowest_listing_price_for_product(game_data=game_data, market_id=city.market_id,
                                                                product_id=product)
            if price is None:
                return None
        income += int(price * value * num_of_productions_made)
    return income


def property_generate_property(game_data: GameData, city_id: str, name: str):
    prop_id = game_data.generate_identifier()
    game_data.properties[prop_id] = Property(city_id=city_id,
                                             name=name,
                                             financial_id=city_id,
                                             size=3)
    return prop_id


def production_loop(game_data: GameData, prop: Property, prop_size: int):
    if prop.production is None:
        return
    if prop.production.num_of_days_remaining is not None:
        if prop.production.num_of_days_remaining > 0:
            prop.production.num_of_days_remaining -= 1
            return
        else:
            prop.production.num_of_days_remaining = None
            _end_production(game_data, prop, prop_size=prop_size)
    _start_production(game_data, prop, prop_size=prop_size)


def assign_production_task(prop: Property, production: Production, storage_in_id: str = None,
                           storage_out_id: str = None, auto_register_market_id: str = None):
    prop.buffs = production.buffs
    prop.production = production
    prop.storage_in_id = storage_in_id
    prop.storage_out_id = storage_out_id
    prop.auto_register_market_id = auto_register_market_id


def _start_procedure(game_data: GameData, prop: Property, prop_size: int) -> bool:
    if 'womole' in prop.buffs:
        if game_data.environment.time.season == 1 or game_data.environment.time.season == 3:
            return False
    if prop.production.consumes is not None:
        if not storage_remove_from_storage(game_data, prop.production.get_consumes(prop_size), prop.storage_in_id):
            return False
    return True


def _start_production(game_data: GameData, prop: Property, prop_size: int):
    if not _start_procedure(game_data, prop, prop_size=prop_size):
        return
    prop.production.start_production()


def get_end_products_after_multiplier(game_data: GameData, production: Production, prop_size: int) -> dict:
    end_multiplier = production.get_multiplier(level=prop_size)
    if 'woliele' in production.buffs:
        buff = game_data.buffs['woliele']
        end_multiplier *= buff.key_effect_data[0]
    if 'wobaole' in production.buffs:
        buff = game_data.buffs['wobaole']
        end_multiplier *= buff.key_effect_data[0]
    return {k: int(v * end_multiplier) for k, v in production.products.items()}


def _end_production(game_data: GameData, prop: Property, prop_size: int):
    end_products = get_end_products_after_multiplier(game_data=game_data, production=prop.production,
                                                     prop_size=prop_size)
    if prop.storage_out_id is None:
        market_id = prop.auto_register_market_id
        if market_id is None:
            market_id = game_data.cities[prop.city_id].market_id
        for product_id, amount in end_products.items():
            city = game_data.cities[prop.city_id]
            price = get_estimated_cost_per_year(game_data=game_data, city=city,
                                                production=prop.production, targeted_level=prop_size)
            price = price / 120 * prop.production.duration / amount
            price = market_get_recommended_pricing(game_data=game_data, market_id=market_id,
                                                   product_id=product_id,
                                                   recommended_price_per_unit=int(price * 1.2),
                                                   bottom_price_per_unit=int(price),
                                                   currency_id=city.currency_id)
            market_register_product(game_data=game_data,
                                    market_id=market_id,
                                    seller_fe_id=prop.financial_id,
                                    product_id=product_id,
                                    amount=amount,
                                    currency_id=city.currency_id,
                                    price_per_unit=price,
                                    is_retail_sale=False,
                                    storage_id=prop.storage_id
                                    )  # remove this
    else:
        storage_add_to_storage(game_data, end_products, prop.storage_out_id)


def get_properties(game_data: GameData, company_fe_id: str) -> dict:
    fetch_result = dict()
    for prop_id, prop in game_data.properties.items():
        if prop.financial_id == company_fe_id:
            fetch_result[prop_id] = prop
    return fetch_result


def property_register_property_for_sale(game_data: GameData, prop_id: str, seller_fe_id: str, price: int = None,
                                        currency_id: str = None, target_buyer_fe_id: str = None):
    if prop_id not in game_data.properties:
        print('register property failed: property not existed')
        return
    prop = game_data.properties[prop_id]
    if prop.financial_id != seller_fe_id:
        print('register property failed: permission denied')
        return
    city = game_data.cities[prop.city_id]
    if currency_id is None:
        currency_id = city.currency_id
    if price is None:
        price = int(city.land_tax_rate * get_employee_salary(population=city.population))
    prop_listing = PropertyListing(city_id=prop.city_id, property_id=prop_id, currency_id=currency_id, price=price,
                                   target_buyer_fe_id=target_buyer_fe_id)
    pl_id = game_data.generate_identifier()
    game_data.property_listings[pl_id] = prop_listing
    return pl_id


def get_properties_by_city(game_data: GameData, city_id: str) -> dict:
    fetch_result = dict()
    for prop_id, prop in game_data.properties.items():
        if prop.city_id == city_id:
            fetch_result[prop_id] = prop
    return fetch_result


def get_property_listings(game_data: GameData, city_id: str) -> dict:
    fetch_result = dict()
    for pl_id, pl in game_data.property_listings.items():
        if pl.city_id == city_id:
            fetch_result[pl_id] = pl
    return fetch_result


def property_purchase_property(game_data: GameData, prop_listing_id: str, buyer_fe_id: str) -> bool:
    if prop_listing_id not in game_data.property_listings:
        print('market_purchase failed: cannot find property listing')
        return False
    prop_listing = game_data.property_listings[prop_listing_id]
    prop = game_data.properties[prop_listing.property_id]
    if prop_listing.target_buyer_fe_id is not None and prop_listing.target_buyer_fe_id != buyer_fe_id:
        print('market_purchase failed: permission denied')
        return False
    if transfer(game_data=game_data, sender_fe_id=buyer_fe_id, receiver_fe_id=prop.financial_id,
                currency_id=prop_listing.currency_id, amount=prop_listing.price):
        prop.financial_id = buyer_fe_id
        property_remove_task(prop=prop)
        del game_data.property_listings[prop_listing_id]
        return True
    return False


def property_remove_task(prop: Property):
    prop.production = None
    prop.storage_out_id = prop.storage_id
    prop.storage_in_id = prop.storage_id
    prop.auto_register_market_id = None
    prop.auto_managed = False
