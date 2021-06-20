from models.TGCommand import TGCommand
from database import db_commands_ref


def send_ping(game_id):
    db_commands_ref.add(TGCommand(cid='gugubird', game_id=game_id, header='env', function='ping').to_dict())
    pass
