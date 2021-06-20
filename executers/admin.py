from data.gameInit import init_game_with_defaults
from database import db_notification_ref, delete_collection, get_db
import json


def initialize_game(command=None):
    get_db().delete()
    init_game_with_defaults(get_db())


def clear_notifications(command=None):
    delete_collection(db_notification_ref, 100)
