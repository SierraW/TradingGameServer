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
from controllers.property_controller import g_new_property, register_property_for_sale


# 0 user / 1 company / 2 heidal_city / 3 country / 4 market / 5 population
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
                  currency_id: str, land_tax_rate: float,
                  market_handle_fee_rate: float, population: Population, productions: list[Production],
                  number_of_initial_property: int) -> str:
    city_id = name
    financial_id = generate_financial_entity(game_data=game_data, name=city_id, entity_type=2)
    city = City(country_id=country_id, name=name, financial_id=financial_id, currency_id=currency_id,
                land_tax_rate=land_tax_rate, population=population)
    city.city_id = city_id
    city.market_id = generate_market(game_data=game_data, name=market_name, financial_name=market_financial_name,
                                     currency_id=currency_id, handling_fee_rate=market_handle_fee_rate,
                                     city_id=city_id)
    city.productions = productions
    game_data.cities[city_id] = city
    for x in range(number_of_initial_property):
        prop_id = g_new_property(game_data, city=city)
        register_property_for_sale(game_data=game_data, prop_id=prop_id, seller_fe_id=financial_id)
    return city_id


def generate_population(game_data: GameData, city_name: str, level_map: list[int], salaries: list[int]) -> Population:
    fe_accounts = [
        generate_financial_entity(game_data=game_data, name=f'{city_name}无产阶级账户', entity_type=5),
        generate_financial_entity(game_data=game_data, name=f'{city_name}中产阶级账户', entity_type=5),
        generate_financial_entity(game_data=game_data, name=f'{city_name}资产阶级账户', entity_type=5),
        generate_financial_entity(game_data=game_data, name=f'{city_name}精英阶级账户', entity_type=5),
    ]
    humans = []
    for i in range(4):
        humans.extend([Human(i) for _ in range(level_map[i])])
    return Population(salaries=salaries, fe_accounts=fe_accounts, humans=humans)


def generate_market(game_data: GameData, city_id: str, name: str, financial_name: str, currency_id: str,
                    handling_fee_rate: float):
    fe = generate_financial_entity(game_data, financial_name, entity_type=4)
    storage = generate_storage(game_data)
    m_id = game_data.generate_identifier()
    game_data.markets[m_id] = Market(market_id=m_id, financial_id=fe, storage_id=storage, city_id=city_id,
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
            '这个单位幸福度为/v'
        ], key_effects_data=[], description=''),
        'woele': Buff(name='饭桶', effects=[
            '这个单位不能一直饿着肚子'
        ], key_effects_data=[], description=''),
        'buff_human_satisfaction': Buff(name='Satisfy', effects=[
            '这个单位的阶级满意度为/v'
        ], key_effects_data=[], description=''),
        # heidal_city buffs
        'buff_city_lvl4_chance': Buff(name='精英人才', effects=[
            '该城市有/v的几率产出精英人才'
        ], key_effects_data=[], description=''),
    }

    # product
    # cat 0: food, 1: lvl_1_consumes
    wheat = generate_product(game_data, '小麦', 0)
    clothes = generate_product(game_data, '布料', 1)

    # consuming
    game_data.environment.human_needs = [
        {
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
                             product_multiplier=[192, 720, 1834, 4000], duration=60, level=0)
    wheat_field.production_multiplier = 1
    wheat_field.buffs = ['wobaole', 'chunxia']
    clothes_factory = Production(name='织布厂', products={clothes: 1},
                                 product_multiplier=[6, 22, 58, 130], duration=2, level=0)

    # country
    calpheon = generate_country(game_data=game_data, name="卡尔佩恩共和国", currency_id=gold, tax_rate=0.14)

    # heidal_city
    generate_city(game_data=game_data, country_id=calpheon, name="海德尔", market_name="海德尔中心市场",
                  market_financial_name="海德尔中心市场账户", currency_id=gold, market_handle_fee_rate=0.05,
                  population=generate_population(game_data=game_data, city_name="海德尔", level_map=[2, 0, 0, 1],
                                                 salaries=[200, 600, 1000, 2000]),
                  productions=[wheat_field, clothes_factory], number_of_initial_property=2,
                  land_tax_rate=120.0)

    # end
