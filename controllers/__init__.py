from models import GameData
from controllers.market_record_controller import init_records
from controllers.market_controller import market_listings_loop


def day_end_loop(game_data: GameData):
    if game_data.environment.time.pause:
        return

    # consume
    #cities_loop(game_data=game_data)

    # record submit
    init_records(game_data=game_data)

    # production.json
    #properties_loop(game_data=game_data)

    # market_listings
    market_listings_loop(game_data=game_data)

    game_data.environment.time.elipse()
