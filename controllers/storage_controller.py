from data import GameData


def remove_from_storage(game_data: GameData, products: dict, storage_id: str) -> bool:
    if storage_id is None or storage_id not in game_data.storages:
        return False
    storage = game_data.storages[storage_id]
    if not storage.remove(products=products):
        return False
    # todo update storage
    return True


def add_to_storage(game_data: GameData, products: dict, storage_id: str) -> bool:
    if storage_id not in game_data.storages:
        return False
    storage = game_data.storages[storage_id]
    for product, amount in products:
        storage.add(product, amount)
    # todo update storage
    return True
