from controllers.storageController import *
from data.GameData import GameData
from models.cities.property.Property import Property


def property_loop(game_data: GameData):
    for item in game_data.properties:
        production_loop(game_data, item)
    pass


def production_loop(game_data: GameData, prop: Property):
    if prop.production.num_of_days_remaining is not None:
        if prop.production.num_of_days_remaining > 0:
            prop.production.num_of_days_remaining -= 1
            return
        else:
            prop.production.num_of_days_remaining = None
            _end_production(game_data, prop)
    _start_production(game_data, prop)


def _start_procedure(game_data: GameData, prop: Property) -> bool:
    if 'womole' in prop.buffs:
        if game_data.environment.time.season == 1 or game_data.environment.time.season == 3:
            return False
    if prop.production.consumes is not None:
        if not remove_from_storage(game_data, prop.production.get_consumes(prop.level), prop.storage_id):
            return False
    return True


def _start_production(game_data: GameData, prop: Property):
    if not _start_procedure(game_data, prop):
        return
    prop.production.start_production()


def _end_production(game_data: GameData, prop: Property):
    end_multiplier = prop.production.get_multiplier(prop.level)
    if 'woliele' in prop.production.buffs:
        end_multiplier *= 0.7
    if 'wobaole' in prop.buffs:
        end_multiplier *= 0.9
    end_products = {k: v * end_multiplier for k, v in prop.production.products.items()}
    add_to_storage(game_data, end_products, prop.storage_id)
