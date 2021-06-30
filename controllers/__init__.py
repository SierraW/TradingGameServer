from models import GameData
from controllers.market_record_controller import init_records
from controllers.city_controller import cities_loop
from controllers.property_controller import properties_loop
from controllers.market_controller import market_listings_loop


def day_end_loop(game_data: GameData):
    # consume
    cities_loop(game_data=game_data)

    # record submit
    init_records(game_data=game_data)

    # production
    properties_loop(game_data=game_data)

    # market_listings
    market_listings_loop(game_data=game_data)
