from controllers.game_init import init_game_with_defaults
from controllers.user_profile_controller import register_user_profile
from models.cities.property.Product import Product
from controllers.market_controller import *
from controllers.company_controller import *
from controllers.property_controller import *

game_data = GameData()
init_game_with_defaults(game_data=game_data)

gold_id = 'GOLD'

print("Register User Profile")
user_a_fe_id = register_user_profile(game_data=game_data, user_identifier='user_a_fe_id', name='user_a_fe_id')
user_b_fe_id = register_user_profile(game_data=game_data, user_identifier='user_b_fe_id', name='user_b_fe_id')

u_a_fe = game_data.financial_entities[user_a_fe_id]
u_b_fe = game_data.financial_entities[user_b_fe_id]

u_a_fe.wallet.currencies[gold_id] = 500000
u_b_fe.wallet.currencies[gold_id] = 100000

heidal_city_id = "海德尔"
heidal_city = game_data.cities[heidal_city_id]

wheat = "小麦"
clothes = "布料"
register_market_listing(game_data=game_data, market_id=heidal_city.market_id, seller_fe_id=user_a_fe_id,
                        product_id=wheat, amount=500, price_per_unit=76)
register_market_listing(game_data=game_data, market_id=heidal_city.market_id, seller_fe_id=user_a_fe_id,
                        product_id=clothes, amount=500, price_per_unit=66)
for listing in game_data.market_listings:
    purchase_single(game_data=game_data, buyer_fe_id=user_b_fe_id, listing_id=listing, amount=50)


com_a_fe_id = company_register_company(game_data=game_data, name="Apple", city_id=heidal_city_id, initial_stock_distribution={
    user_a_fe_id: 9000,
    user_b_fe_id: 1000
}, fund_distribution={
    user_a_fe_id: 100000
})
print(com_a_fe_id)
com_a_fe = game_data.financial_entities[com_a_fe_id]
print(com_a_fe)


print("Purchase test successful A")
print(game_data.financial_entities[com_a_fe_id].wallet)
print(game_data.property_listings)
print(get_properties(game_data=game_data, company_fe_id=com_a_fe_id))
pls = [lid for lid in game_data.property_listings]
for listing_id in pls:
    print(property_purchase_property(game_data=game_data, prop_listing_id=listing_id, buyer_fe_id=com_a_fe_id))
print(game_data.financial_entities[com_a_fe_id].wallet)
print(game_data.property_listings)
print(get_properties(game_data=game_data, company_fe_id=com_a_fe_id))

properties_loop(game_data=game_data)

print(get_properties(game_data=game_data, company_fe_id=com_a_fe_id))

production = None
for pd in heidal_city.productions:
    print(pd)
    print('level 0')
    cost = get_estimated_cost_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=0)
    earn = get_estimated_income_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=0)
    print(f'estimated cost: {cost}')
    print(f'estimated earn: {earn}')
    print(f'ratio: {earn / cost * 100}')

    print('level 1')
    cost = get_estimated_cost_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=1)
    earn = get_estimated_income_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=1)
    print(f'estimated cost: {cost}')
    print(f'estimated earn: {earn}')
    print(f'ratio: {earn / cost * 100}')

    print('level 2')
    cost = get_estimated_cost_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=2)
    earn = get_estimated_income_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=2)
    print(f'estimated cost: {cost}')
    print(f'estimated earn: {earn}')
    print(f'ratio: {earn / cost * 100}')

    print('level 3')
    cost = get_estimated_cost_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=3)
    earn = get_estimated_income_per_year(game_data=game_data, city_id=heidal_city_id, production=pd, targeted_level=3)
    print(f'estimated cost: {cost}')
    print(f'estimated earn: {earn}')
    print(f'ratio: {earn / cost * 100}')
