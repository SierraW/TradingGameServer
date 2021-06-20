from data import get_game_data
from models.TGCommand import TGCommand
from .environment import *
from .admin import *
from database import db_notification_ref

env_options = {
    'u_token_service': user_token_service,
    'ping': ping
}

admin_options = {
    'initialize': init_game_with_defaults
}

header_options = {
    'env': env_options,
    'admin': admin_options
}


def check_auth(command) -> bool:
    return True


def check_admin(command) -> bool:
    return True


def _execute(command: TGCommand):
    if command.header in header_options:
        if command.function in header_options[command.header]:
            response = header_options[command.header][command.function](command.payload)
            command.payload = response if response is not None else {'success': True}
            send(command)
    pass


def execute(command):
    if not check_auth(command):
        pass
    command = TGCommand.from_dict(command)
    if command.header == 'admin' and not check_admin(command):
        pass
    _execute(command)


def send(notification: TGCommand):
    db_notification_ref.add(notification.to_dict())
