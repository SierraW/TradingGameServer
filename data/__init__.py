from models.GameData import GameData

game_data_storage = dict()


def get_game_data(game_id: str):
    if game_id not in game_data_storage:
        game_data_storage[game_id] = GameData.from_cloud(game_id)
    return game_data_storage[game_id]
