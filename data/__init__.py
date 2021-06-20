from data.GameData import GameData
from data.gameInit import init_game_with_defaults


game_data_storage = dict()


def get_game_data(game_id: str):
    if game_id not in game_data_storage:
        game_data_storage[game_id] = GameData.from_cloud(game_id)
    return game_data_storage[game_id]
