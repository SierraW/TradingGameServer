import json

from controllers.game_initialize_controller import init_from_local_essential
from models.GameData import GameData
from controllers.population_v2_controller import *

game_data = GameData()

init_from_local_essential(game_data=game_data)

population_loop(game_data=game_data)
