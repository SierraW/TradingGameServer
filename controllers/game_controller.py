from data import get_game_data
from database import *
from controllers.property_controller import property_loop
from controllers.city_controller import cities_loop


def records_loop():
    docs = db.collection(servers).stream()
    for doc in docs:
        game_loop(doc.id)


def game_loop(game_id):
    game_data = get_game_data(game_id)
    cities_loop(game_data)
    property_loop(game_data)
