from data import GameData
from models.UserProfile import UserProfile
from controllers.financial_controller import register_financial_entity


def verify_user_account(game_data: GameData, user_identifier: str) -> bool:
    return user_identifier in game_data.user_profiles


def register_user_profile(game_data: GameData, user_identifier: str, name: str):
    if verify_user_account(game_data=game_data, user_identifier=user_identifier):
        return None
    fe_id = register_financial_entity(game_data=game_data, name=name, entity_type=0)
    game_data.user_profiles[user_identifier] = UserProfile(financial_id=fe_id)
    return fe_id
