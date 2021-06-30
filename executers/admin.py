from controllers.game_init import init_game_with_defaults
from database import db_notification_ref, delete_collection, get_db


def initialize_game(command=None):
    get_db().delete()
    init_game_with_defaults(get_db())


def clear_notifications(command=None):
    delete_collection(db_notification_ref, 100)
