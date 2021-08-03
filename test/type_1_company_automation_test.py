from controllers.game_init import init_game_with_defaults
from controllers.user_profile_controller import register_user_profile
from models.cities.property.Product import Product
from controllers.market_controller import *
from controllers.market_record_controller import *
from controllers.property_controller import *
from controllers.storage_controller import *
from controllers.company_controller import *

game_data = GameData()
init_game_with_defaults(game_data=game_data)
init_records(game_data=game_data)

gold_id = 'GOLD'
heidal_city_id = "海德尔"
wheat = "小麦"
clothes = "布料"
market_id = '8'

print("Register User Profile")
user_a = register_user_profile(game_data=game_data, user_identifier='user_a_fe_id', name='user_a_fe_id')
user_b = register_user_profile(game_data=game_data, user_identifier='user_b_fe_id', name='user_b_fe_id')
u_a_fe = game_data.financial_entities[user_a]
u_b_fe = game_data.financial_entities[user_b]

u_a_fe.wallet.currencies[gold_id] = 500000
u_b_fe.wallet.currencies[gold_id] = 500000

company_a_id = company_register_company(game_data=game_data,
                                        name="Company A",
                                        city_id=heidal_city_id,
                                        initial_stock_distribution={user_a: 10000},
                                        fund_distribution={user_a: 500000},
                                        company_type=0,
                                        auto_managed=False)

company_b_id = company_register_company(game_data=game_data,
                                        name="Company B",
                                        city_id=heidal_city_id,
                                        initial_stock_distribution={user_b: 10000},
                                        fund_distribution={user_b: 500000},
                                        company_type=1,
                                        auto_managed=False)

company_a = company_get_company(game_data=game_data, company_id=company_a_id)
company_b = company_get_company(game_data=game_data, company_id=company_b_id)

company_a_fe = game_data.financial_entities[company_a_id]
company_b_fe = game_data.financial_entities[company_b_id]

print(property_purchase_property(game_data=game_data, prop_listing_id='10', buyer_fe_id=company_a_id))
print(property_purchase_property(game_data=game_data, prop_listing_id='12', buyer_fe_id=company_b_id))

print(company_register_property(game_data=game_data, company_id=company_a_id, prop_id='9'))
print(company_register_property(game_data=game_data, company_id=company_b_id, prop_id='11'))

property_a = game_data.properties['9']
property_b = game_data.properties['11']
storage_a = game_data.storages['9']
storage_b = game_data.storages['11']

print(storage_add_to_storage(game_data=game_data, products={wheat: 10000}, storage_id=company_a.property_id))

print('register product to wholesale market')
print(market_register_product(game_data=game_data, market_id=market_id, seller_fe_id=company_a_id, product_id=wheat,
                              amount=500, currency_id=gold_id, price_per_unit=100, is_retail_sale=False,
                              storage_id=company_a.property_id))

print(market_register_product(game_data=game_data, market_id=market_id, seller_fe_id=company_a_id, product_id=wheat,
                              amount=1500, currency_id=gold_id, price_per_unit=100, is_retail_sale=False,
                              storage_id=company_a.property_id))


company_b.auto_managed = True
companies_loop(game_data=game_data)
companies_loop(game_data=game_data)
