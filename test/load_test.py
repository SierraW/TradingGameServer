from controllers.game_initialize_controller import init_from_local_essential
from models.GameData import GameData

game_data = GameData()

init_from_local_essential(game_data=game_data)
