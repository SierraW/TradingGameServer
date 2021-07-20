from controllers import init_records
from controllers.game_init import init_game_with_defaults
from controllers.user_profile_controller import register_user_profile
from models.cities.property.Product import Product
from controllers.market_controller import *
from controllers.company_controller import *
from controllers.property_controller import *
from controllers.population_controller import *
from controllers.city_controller import *

game_data = GameData()
init_game_with_defaults(game_data=game_data)

gold_id = 'GOLD'

print("Register User Profile")
user_a_fe_id = register_user_profile(game_data=game_data, user_identifier='user_a_fe_id', name='user_a_fe_id')
user_b_fe_id = register_user_profile(game_data=game_data, user_identifier='user_b_fe_id', name='user_b_fe_id')

u_a_fe = game_data.financial_entities[user_a_fe_id]
u_b_fe = game_data.financial_entities[user_b_fe_id]

u_a_fe.wallet.currencies[gold_id] = 50000000
u_b_fe.wallet.currencies[gold_id] = 100000

heidal_city_id = "海德尔"
heidal_city = game_data.cities[heidal_city_id]
heidal_city_fe = game_data.financial_entities[heidal_city.financial_id]

heidal_city_market = game_data.markets[heidal_city.market_id]
heidal_city_market_fe = game_data.financial_entities[heidal_city_market.financial_id]

wheat = "小麦"
clothes = "布料"
register_market_listing(game_data=game_data, market_id=heidal_city.market_id, seller_fe_id=user_a_fe_id,
                        product_id=wheat, amount=500, price_per_unit=100, currency_id=gold_id, auto_register=True)
register_market_listing(game_data=game_data, market_id=heidal_city.market_id, seller_fe_id=user_a_fe_id,
                        product_id=clothes, amount=2, price_per_unit=90, currency_id=gold_id, auto_register=True)



com_a_fe_id = register_company(game_data=game_data, name="Apple", city_id=heidal_city_id, initial_stock_distribution={
    user_a_fe_id: 9000,
    user_b_fe_id: 1000
}, fund_distribution={
    user_a_fe_id: 100000
}, auto_managed=False)
print(com_a_fe_id)
com_a_fe = game_data.financial_entities[com_a_fe_id]
print(com_a_fe)

transfer(game_data=game_data, sender_fe_id=user_a_fe_id, receiver_fe_id=heidal_city.financial_id,
         currency_id=heidal_city.currency_id, amount=3000000)

for _ in range(360):
    init_records(game_data=game_data)
    population_loop(game_data=game_data, city=heidal_city)
    market_listings_loop(game_data=game_data)
    cities_loop(game_data=game_data)
    companies_loop(game_data=game_data)
    properties_loop(game_data=game_data)
    game_data.environment.time.elapsed()

print(purchase_by_category(game_data=game_data, buyer_fe_id=heidal_city.financial_id, category=0, amount_required=50,
                           market_id=heidal_city.market_id,
                           available_budget=500).__str__())

print(heidal_city_market)

