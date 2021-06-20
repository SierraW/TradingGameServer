from data import GameData
from database import get_db, storages


def remove_from_storage(game_data: GameData, products: dict, storage_id: str) -> bool:
    if storage_id not in game_data.storages:
        return False
    storage = game_data.storages[storage_id]
    items_removed = dict()
    for product, amount in products.items():
        if storage.remove(product, amount):
            items_removed[product] = amount
        else:
            add_to_storage(game_data, items_removed, storage_id)
            return False
    get_db(game_data.identifier, storages).set({k: storage[k] for k in products}, merge=True)
    return True


def add_to_storage(game_data: GameData, products: dict, storage_id: str) -> bool:
    if storage_id not in game_data.storages:
        return False
    storage = game_data.storages[storage_id]
    for product, amount in products:
        storage.add(product, amount)
    get_db(game_data.identifier, storages).set({k: storage[k] for k in products}, merge=True)
    return True
