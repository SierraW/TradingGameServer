from data import get_game_data
from database import *
from controllers.propertyController import property_loop
from controllers.cityController import cities_loop


def records_loop():
    docs = db.collection(servers).stream()
    for doc in docs:
        game_loop(doc.id)


def game_loop(game_id):
    game_data = get_game_data(game_id)
    cities_loop(game_data)
    property_loop(game_data)
