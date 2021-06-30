from controllers.game_init import init_game_with_defaults
from controllers.user_profile_controller import register_user_profile
from controllers.financial_controller import *

game_data = GameData()
init_game_with_defaults(game_data=game_data)

gold_id = 'GOLD'

print("Register User Profile")
urer_a = register_user_profile(game_data=game_data, user_identifier='urer_a', name='urer_a')
urer_b = register_user_profile(game_data=game_data, user_identifier='urer_b', name='urer_b')

u_a_fe = game_data.financial_entities[urer_a]
u_b_fe = game_data.financial_entities[urer_b]

u_a_fe.wallet.currencies[gold_id] = 500000

print("TestFailed")
print("before")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
transfer(game_data=game_data, sender_fe_id=urer_b, receiver_fe_id=urer_a, currency_id=gold_id, amount=100)
print("after")
print(u_a_fe.wallet)
print(u_b_fe.wallet)

print("TestSuccess")
print("before")
print(u_a_fe.wallet)
print(u_b_fe.wallet)
transfer(game_data=game_data, sender_fe_id=urer_a, receiver_fe_id=urer_b, currency_id=gold_id, amount=10)
print("after")
print(u_a_fe.wallet)
print(u_b_fe.wallet)

print("transactions")
print(u_a_fe.wallet.transactions)
print(u_b_fe.wallet.transactions)
