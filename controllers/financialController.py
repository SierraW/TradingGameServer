from data import GameData


def transfer(game_data: GameData, sender_fe_id: str, receiver_fe_id: str, currency_id, amount) -> bool:
    if sender_fe_id in game_data.financial_entities and receiver_fe_id in game_data.financial_entities:
        sender_fe = game_data.financial_entities[sender_fe_id]
        receiver_fe = game_data.financial_entities[receiver_fe_id]
        if sender_fe.wallet.pay(currency_id=currency_id, amount=amount):
            receiver_fe.wallet.receive(currency_id=currency_id, amount=amount)
            return True
    return False
