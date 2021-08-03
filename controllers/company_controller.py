from controllers.company_automation_controller import *
from controllers.financial_controller import verify, register_financial_entity, transfer, remove_financial_entity
from controllers.property_controller import get_properties, get_employees, property_loop, get_estimated_cost_per_year, \
    get_employee_salary, property_remove_task
from controllers.stock_controller import stock_arrange_initial_stock
from data import GameData
from models.Company import Company
from models.cities.City import City


def company_get_company(game_data: GameData, company_id: str) -> Company:
    return game_data.companies[company_id]


def companies_loop(game_data: GameData):
    for com_id, company in game_data.companies.items():
        company_loop(game_data=game_data, company=company)


def company_loop(game_data: GameData, company: Company):
    city = game_data.cities[company.city_id]
    if city is None:
        return
    # make a payment
    property_dict = get_properties(game_data=game_data, company_fe_id=company.financial_id)
    payment = 0
    for prop_id, prop in property_dict.items():
        # salaries
        employee_list = get_employees(population=city.population, prop_id=prop_id)
        for human in employee_list:
            salary = get_employee_salary(population=city.population, level=human.level)
            if transfer(game_data=game_data, sender_fe_id=company.financial_id, receiver_fe_id=city.financial_id,
                        currency_id=city.currency_id, amount=salary):
                payment += salary
            else:
                human.property_id = None
        property_loop(game_data=game_data, prop_id=prop_id, prop=prop, company=company)
    if company.auto_managed:
        if company.company_type == 0:
            type_0_company_automation(game_data=game_data, company=company, property_dict=property_dict)
        elif company.company_type == 1:
            type_1_company_automation(game_data=game_data, company=company)
    pass


def company_calculate_minimum_budget_for_a_year(game_data: GameData, city: City) -> int:
    minimum_budget = -1
    for production in city.productions:
        budget = get_estimated_cost_per_year(game_data=game_data, city=city, production=production, targeted_level=0)
        if minimum_budget < 0 or budget < minimum_budget:
            minimum_budget = budget
    return minimum_budget


# company_type: 0 normal, 1 retail company (food only)
def company_register_company(game_data: GameData, name: str, city_id: str, initial_stock_distribution: dict,
                             fund_distribution: dict, company_type: int, auto_managed: bool,
                             property_listings: list[str] = None):
    total_stock = 0
    for fe_id, stock in initial_stock_distribution.items():
        if verify(game_data=game_data, fe_id=fe_id):
            total_stock += stock
        else:
            return None
    if total_stock == 0:
        return None
    city = game_data.cities[city_id]
    financial_id = register_financial_entity(game_data=game_data, name=name, entity_type=1)
    transferred = dict()
    for fe_id, fund in fund_distribution.items():
        if fe_id not in initial_stock_distribution:
            return None
        if transfer(game_data=game_data, sender_fe_id=fe_id, receiver_fe_id=financial_id, currency_id=city.currency_id,
                    amount=fund):
            transferred[fe_id] = fund
        else:
            for fe_id_1, amount in transferred.items():
                transfer(game_data=game_data, sender_fe_id=financial_id, receiver_fe_id=fe_id_1,
                         currency_id=city.currency_id,
                         amount=amount)
            remove_financial_entity(game_data=game_data, fe_id=financial_id)
            return None
    company = Company(financial_id=financial_id, city_id=city_id, total_stock=total_stock, auto_managed=auto_managed,
                      t_plus_created=game_data.environment.time.get_t_plus_from_now(), company_type=company_type)
    game_data.companies[financial_id] = company

    stock_arrange_initial_stock(game_data=game_data, company_id=financial_id,
                                initial_stock_distribution=initial_stock_distribution)

    if property_listings is not None:
        for prop_listing_id in property_listings:
            property_purchase_property(game_data=game_data, prop_listing_id=prop_listing_id, buyer_fe_id=financial_id)
    return financial_id


def company_register_property(game_data: GameData, company_id: str, prop_id: str) -> bool:
    company = game_data.companies[company_id]
    prop = game_data.properties[prop_id]
    if prop.financial_id == company.financial_id:
        property_remove_task(prop=prop)
        company.property_id = prop_id
        return True
    else:
        return False
