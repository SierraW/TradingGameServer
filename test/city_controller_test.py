from controllers.game_init import init_game_with_defaults
from controllers.user_profile_controller import register_user_profile
from models.cities.property.Product import Product
from controllers.market_controller import *

game_data = GameData()
init_game_with_defaults(game_data=game_data)

gold_id = 'GOLD'

print("Register User Profile")
urer_a = register_user_profile(game_data=game_data, user_identifier='user_a_fe_id', name='user_a_fe_id')
urer_b = register_user_profile(game_data=game_data, user_identifier='user_b_fe_id', name='user_b_fe_id')

u_a_fe = game_data.financial_entities[urer_a]
u_b_fe = game_data.financial_entities[urer_b]

u_a_fe.wallet.currencies[gold_id] = 500000

apple = "小麦"
game_data.products[apple] = Product(apple, 0)

market_id = None
for mid in game_data.markets:
    market_id = mid

print("Market ID:")
print(market_id)

print("listing test")
print(game_data.market_listings)
register_market_listing(game_data=game_data, market_id=market_id, seller_fe_id=urer_b, product_id=apple, amount=500,
                        price_per_unit=100)
print(game_data.market_listings)


print("purchase test")
print("TestFailed budget b-in")
print("before")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
purchase(game_data=game_data, buyer_fe_id=urer_b, products={apple: 100}, market_id=market_id, budget=1)
print("after")
print(u_a_fe.wallet)
print(u_b_fe.wallet)

print("TestFailed b-out")
print("before")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
purchase(game_data=game_data, buyer_fe_id=urer_b, products={apple: 100}, market_id=market_id, budget=100)
print("after")
print(u_a_fe.wallet)
print(u_b_fe.wallet)

print("TestSuccess A")
print("before")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
purchase(game_data=game_data, buyer_fe_id=urer_a, products={apple: 10}, market_id=market_id, budget=50000)
print("after")
print(u_a_fe.wallet)
print(u_b_fe.wallet)

print(game_data.market_listings)

print("TestSuccess B")
print("before")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
purchase(game_data=game_data, buyer_fe_id=urer_a, products={apple: 500}, market_id=market_id, budget=50000)
print("after")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
print(game_data.financial_entities['4'].wallet)

print(game_data.market_listings)

print("transactions")
print(u_a_fe.wallet.transactions)
print(u_b_fe.wallet.transactions)

print(game_data.market_reports)
print(get_previous_average_price(game_data=game_data, market_id=market_id, product_id=apple, currency_id=gold_id))
