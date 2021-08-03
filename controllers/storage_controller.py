from controllers.product_controller import product_get_products_by_category
from data import GameData
from models.Storage import Storage


def storage_remove_from_storage(game_data: GameData, products: dict, storage_id: str) -> bool:
    if storage_id is None or storage_id not in game_data.storages:
        print(f'Cannot find storage with id {storage_id}')
        return False
    storage = game_data.storages[storage_id]
    if not storage.remove(products=products):
        return False
    # todo update storage
    return True


def storage_add_to_storage(game_data: GameData, products: dict, storage_id: str) -> bool:
    if storage_id not in game_data.storages:
        print(f'Cannot find storage with id {storage_id}')
        return False
    storage = game_data.storages[storage_id]
    for product, amount in products.items():
        storage.add(product, amount)
    # todo update storage
    return True


def storage_check_storage_by_type(game_data: GameData, storage_id: str, category: int) -> int:
    storage = game_data.storages[storage_id]
    count = 0
    products = product_get_products_by_category(game_data=game_data, category=category)
    for pid in products:
        if pid in storage.products:
            count += storage.products[pid]
    return count


def storage_verify_product(game_data: GameData, storage_id: str, product_id: str) -> int:
    storage = game_data.storages[storage_id]
    if product_id in storage.products:
        return storage.products[product_id]
    return 0


def storage_check_storage_by_product_id(game_data: GameData, storage_id: str, product_id: str) -> int:
    storage = game_data.storages[storage_id]
    return storage.products[product_id] if product_id in storage.products else 0


def storage_find_sub_storages(game_data: GameData, location: str) -> dict:
    return dict(filter(lambda storage: storage.location == location, game_data.storages.items()))


def storage_get_storage(game_data: GameData, storage_id: str) -> Storage:
    return game_data.storages[storage_id]


def storage_get_products_by_category(game_data: GameData, storage_id: str, category: int) -> dict:
    products_dict = dict()
    storage = game_data.storages[storage_id]
    products_needed = product_get_products_by_category(game_data=game_data, category=category)
    for pid, product in products_needed.items():
        if pid in storage.products:
            products_dict[pid] = storage.products[pid]
    return products_dict


# def storage_rent_a_storage(game_data: GameData, company_id: str) -> str:
#     company = game_data.companies[company_id]
#     city = game_data.cities[company.city_id]
#     storage_dict = find_sub_storages(game_data=game_data, storage_id=city.market_id)
#     for storage_id, storage in storage_dict.items():
#         if storage.owner_fe_id == company_id:
#             return storage_id


def storage_create_a_storage(game_data: GameData, city_id: str, location: str, owner_fe_id: str) -> str:
    if location in game_data.storages:
        return location
    game_data.storages[location] = Storage(owner_fe_id=owner_fe_id, location=location, city_id=city_id)
    return location
