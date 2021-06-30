from models.GameData import GameData
from models.Buff import Buff
from models.FinancialEntity import FinancialEntity
from models.Human import Human
from models.TGEnviroment import TGEnvironment
from models.cities.Market import Market
from models.cities.Population import Population
from models.geometry.Currency import Currency
from models.cities.City import City
from models.geometry.Country import Country
from models.cities.property.Product import Product
from models.cities.property.Production import Production
from models.Storage import Storage
from controllers.property_controller import g_new_property


# 0 user / 1 company / 2 city / 3 country / 4 market
def generate_financial_entity(game_data: GameData, name: str, entity_type: int) -> str:
    fe = FinancialEntity(name=name, entity_type=entity_type)
    fe_id = game_data.generate_identifier()
    game_data.financial_entities[fe_id] = fe
    return fe_id


def generate_storage(game_data: GameData) -> str:
    st_id = game_data.generate_identifier()
    game_data.storages[st_id] = Storage()
    return st_id


def generate_country(game_data: GameData, name: str, currency_id: str, tax_rate: float) -> str:
    country = Country(name=name, currency_id=currency_id, tax_rate=tax_rate)
    country_id = game_data.generate_identifier()
    game_data.countries[country_id] = country
    return country_id


def generate_city(game_data: GameData, country_id: str, name: str, market_name: str, market_financial_name: str,
                  currency_id: str,
                  market_handle_fee_rate: float, population: Population, productions: list[Production],
                  number_of_initial_property: int) -> str:
    city_id = game_data.generate_identifier()
    city = City(country_id=country_id, name=name, financial_id=game_data.generate_identifier(), currency_id=currency_id)
    city.city_id = city_id
    city.market_id = generate_market(game_data, market_name, market_financial_name, currency_id, market_handle_fee_rate)
    city.population = population
    city.productions = productions
    game_data.cities[city_id] = city
    for x in range(number_of_initial_property):
        g_new_property(game_data, city=city)
    return city_id


def add_city(game_data: GameData, city: City) -> str:
    ci_id = game_data.generate_identifier()
    game_data.cities[ci_id] = city
    return ci_id


def generate_market(game_data: GameData, name: str, financial_name: str, currency_id: str, handling_fee_rate: float):
    fe = generate_financial_entity(game_data, financial_name, entity_type=4)
    storage = generate_storage(game_data)
    m_id = game_data.generate_identifier()
    game_data.markets[m_id] = Market(market_id=m_id, financial_id=fe, storage_id=storage,
                                     name=name, currency_id=currency_id, handling_fee_rate=handling_fee_rate)
    return m_id


def generate_product(game_data: GameData, name: str, category: int) -> str:
    game_data.products[name] = Product(name, category)
    return name


def generate_currency(game_data: GameData, name: str, prefix: str, symbol: str) -> str:
    game_data.currencies[prefix] = Currency(name, prefix, symbol)
    return prefix


def init_game_with_defaults(game_data: GameData):
    # time
    game_data.environment = TGEnvironment()

    # currency
    gold = generate_currency(game_data, name='Gold', prefix='GOLD', symbol='G')

    # buffs
    game_data.buffs = {
        # property buffs
        'wobaole': Buff(name='自给自足', effects=[
            '这个单位产出修正为/$', '这个单位的职员无需购买食物'
        ], key_effects_data=[0.9], description=''),
        'womole': Buff(name='适时耕种', effects=[
            '这个单位仅能在春季或者秋季开始生产'
        ], key_effects_data=[], description=''),
        'woliele': Buff(name='干旱', effects=[
            '这个单位因为曾经经历干旱而导致减产'
        ], key_effects_data=[0.7], description=''),
        # human buffs
        'wohaole': Buff(name='生物', effects=[
            '这个单位需要食物才能繁衍生息'
        ], key_effects_data=[], description=''),
        'woele': Buff(name='饭桶', effects=[
            '这个单位不能一直饿着肚子'
        ], key_effects_data=[], description=''),
    }

    # product
    # cat 0: food, 1: lvl_1_consumes
    wheat = generate_product(game_data, '小麦', 0)
    clothes = generate_product(game_data, '布料', 1)

    # consuming
    game_data.environment.human_needs = [
        {
            wheat: 1,
            clothes: 1
        },
        {
            wheat: 1,
            clothes: 1
        },
        {
            wheat: 1,
            clothes: 1
        },
        {
            wheat: 1,
            clothes: 1
        },
    ]

    # production
    wheat_field = Production(name='小麦田', products={wheat: 1},
                             size_multiplier=[96, 360, 917, 1080], duration=60, level=0)
    wheat_field.production_multiplier = 1
    wheat_field.buffs = ['wobaole', 'chunxia']
    clothes_factory = Production(name='织布厂', products={clothes: 1},
                                 size_multiplier=[3, 11, 29, 34], duration=2, level=0)

    # country
    calpheon = generate_country(game_data=game_data, name="卡尔佩恩共和国", currency_id=gold, tax_rate=0.14)

    # city
    generate_city(game_data=game_data, country_id=calpheon, name="海德尔", market_name="海德尔中心市场",
                  market_financial_name="海德尔中心市场账户", currency_id=gold, market_handle_fee_rate=0.05,
                  population=Population(humans=[Human(level=0), Human(level=0)]),
                  productions=[wheat_field, clothes_factory], number_of_initial_property=2)
