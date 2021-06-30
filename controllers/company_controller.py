from data import GameData
from models.Company import Company
from financial_controller import verify, count, transfer
from models.FinancialEntity import FinancialEntity
from city_controller import get_city
from models.cities.City import City
from property_controller import get_properties, get_employees, property_loop, purchase_property


def company_loop(game_data: GameData, company: Company):
    city = get_city(game_data=game_data, city_id=company.city_id)
    if city is None:
        return
    # make a payment
    property_dict = get_properties(game_data=game_data, company=company)
    payment = 0
    for prop_id, prop in property_dict.items():
        employee_list = get_employees(population=city.population, prop_id=prop_id)
        for human in employee_list:
            if transfer(game_data=game_data, sender_fe_id=company.financial_id, receiver_fe_id=city.financial_id,
                        currency_id=city.currency_id, amount=human.salary):
                payment += human.salary
            else:
                human.property_id = None
        property_loop(game_data=game_data, prop_id=prop_id, prop=prop, company=company)
    calculate_budget_cap(city=city, fe=game_data.financial_entities[company.financial_id], company=company,
                         daily_payment=payment)
    pass


def calculate_budget_cap(city: City, fe: FinancialEntity, company: Company, daily_payment: int):
    total_amount_of_money = fe.wallet.check(currency_id=city.currency_id)
    budget = total_amount_of_money - (daily_payment * 120)
    if budget > 0:
        company.budget_cap = budget
    else:
        company.budget_cap = 0


def register_company(game_data: GameData, name: str, city_id: str, initial_stock_distribution: dict,
                     property_listings: list[str] = None):
    total_stock = 0
    for fe_id, stock in initial_stock_distribution.items():
        if verify(game_data=game_data, fe_id=fe_id):
            total_stock += stock
        else:
            return None
    financial_id = game_data.generate_identifier()
    game_data.financial_entities = FinancialEntity(name=name, entity_type=1)
    company = Company(financial_id=financial_id, city_id=city_id, total_stock=total_stock)
    game_data.companies[financial_id] = company
    if property_listings is not None:
        for prop_listing_id in property_listings:
            purchase_property(game_data=game_data, prop_listing_id=prop_listing_id, buyer_fe_id=financial_id)
    return financial_id
