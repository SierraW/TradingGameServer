import json


with open('../storage/game_config.json', 'r') as f:
    data = json.load(f)
    print(data)
    print(data['game_env'])