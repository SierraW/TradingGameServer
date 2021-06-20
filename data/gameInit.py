from data.GameData import GameData
from models.Buff import Buff
from models.FinancialEntity import FinancialEntity
from models.Human import Human
from models.TGEnviroment import TGEnvironment
from models.TGTime import TGTime
from models.cities.Market import Market
from models.cities.Population import Population
from models.geometry.Currency import Currency
from models.cities.City import City
from models.geometry.Country import Country
from models.cities.property.Property import Property
from models.cities.property.Product import Product
from models.cities.property.Production import Production
from models.Storage import Storage


def generate_financial_entity(game_data: GameData, name: str = '人') -> str:
    fe = FinancialEntity(name=name)
    fe_id = game_data.generate_identifier()
    game_data.financial_entities[fe_id] = fe
    return fe_id


def generate_storage(game_data: GameData) -> str:
    st_id = game_data.generate_identifier()
    game_data.storages[st_id] = Storage()
    return st_id


def add_city(game_data: GameData, city: City) -> str:
    ci_id = game_data.generate_identifier()
    game_data.cities[ci_id] = city
    return ci_id


def generate_market(game_data: GameData, name: str, financial_name: str, handling_fee_rate: float):
    fe = generate_financial_entity(game_data, financial_name)
    storage = generate_storage(game_data)
    m_id = game_data.generate_identifier()
    return Market(market_id=m_id, financial_id=fe, storage_id=storage,
                  name=name, handling_fee_rate=handling_fee_rate)


def generate_property(game_data: GameData, city_id: str, name: str) -> str:
    prop_id = game_data.generate_identifier()
    game_data.properties[prop_id] = Property(city_id, name)
    return prop_id


def generate_product(game_data: GameData, name: str, category: str) -> str:
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
        'wobaole': Buff(name='自给自足', effects=[
            '这个单位产出修正为90%', '这个单位的职员无需购买食物'
        ], description=''),
        'womole': Buff(name='适时耕种', effects=[
            '这个单位仅能在春季或者秋季开始生产'
        ], description=''),
        'woliele': Buff(name='干旱', effects=[
            '这个单位因为曾经经历干旱而导致减产'
        ], description=''),
    }

    # product
    wheat = generate_product(game_data, '小麦', '食物')
    clothes = generate_product(game_data, '布料', '布制品')

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
                             level_multiplier=[96, 360, 917, 1080], duration=60)
    wheat_field.production_multiplier = 1
    wheat_field.buffs = ['wobaole', 'chunxia']
    clothes_factory = Production(name='织布厂', products={clothes: 1},
                                 level_multiplier=[3, 11, 29, 34], duration=2)

    # city
    heidel = City(name="海德尔")
    heidel.market = generate_market(game_data, '海德尔中心市场', '海德尔中心市场账户', 0.15)
    heidel.population = [Human(1, 0), Human(1, 0)]
    heidel.productions = [wheat_field, clothes_factory]
    heidel_id = add_city(game_data, heidel)
    for x in range(17):
        generate_property(game_data, city_id=heidel_id, name=f'{x}号')

    # country
    calpheon = Country(name="卡尔佩恩共和国", currency=gold, tax_rate=0.14)

    game_data.countries.append(calpheon)
