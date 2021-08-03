from controllers.game_init import init_game_with_defaults
from controllers.storage_controller import *


game_data = GameData()
init_game_with_defaults(game_data=game_data)

property_a = "test_storage_a"
property_b = "test_storage_b"

wheat = "小麦"
clothes = "布料"

storage_a_id = storage_create_a_storage(game_data=game_data, location=property_a, owner_fe_id="tester_a", city_id="a")
storage_b_id = storage_create_a_storage(game_data=game_data, location=property_b, owner_fe_id="tester_b", city_id="a")

print(storage_get_storage(game_data=game_data, storage_id=property_a))

storage_add_to_storage(game_data=game_data, products={wheat: 123}, storage_id=storage_a_id)

print(storage_get_storage(game_data=game_data, storage_id=property_a))

print(storage_remove_from_storage(game_data=game_data, products={wheat: 12}, storage_id=storage_a_id))

print(storage_get_storage(game_data=game_data, storage_id=property_a))

print(storage_remove_from_storage(game_data=game_data, products={wheat: 120}, storage_id=storage_a_id))

print(storage_get_storage(game_data=game_data, storage_id=property_a))

storage_add_to_storage(game_data=game_data, products={clothes: 123}, storage_id=storage_a_id)
storage_add_to_storage(game_data=game_data, products={clothes: 123}, storage_id=storage_b_id)

print(storage_check_storage_by_type(game_data=game_data, storage_id=storage_a_id, category=0))
print(storage_check_storage_by_type(game_data=game_data, storage_id=storage_a_id, category=1))
print(storage_check_storage_by_product_id(game_data=game_data, storage_id=storage_a_id, product_id=wheat))
print(storage_check_storage_by_product_id(game_data=game_data, storage_id=storage_b_id, product_id=wheat))
print(storage_get_products_by_category(game_data=game_data, storage_id=storage_a_id, category=0))
