from data import GameData
from models.FinancialEntity import FinancialEntity
from models.cities.personality.Population import Population
from models.report.Transaction import Transaction


def get_population_fe_id(population: Population, level: int) -> str:
    return population.fe_accounts[level]


def financial_get_financial_entity(game_data: GameData, financial_id: str) -> FinancialEntity:
    return game_data.financial_entities[financial_id]


def register_financial_entity(game_data: GameData, name: str, entity_type: int, currency_dict: dict = None) -> str:
    fe = FinancialEntity(name=name, entity_type=entity_type, currency_dict=currency_dict)
    fe_id = game_data.generate_identifier()
    game_data.financial_entities[fe_id] = fe
    return fe_id


def remove_financial_entity(game_data: GameData, fe_id: str) -> bool:
    if fe_id not in game_data.financial_entities:
        return False
    fe = game_data.financial_entities[fe_id]
    wallet = fe.wallet
    for _, amount in wallet.currencies:
        if amount > 0:
            return False
    del game_data.financial_entities[fe_id]
    return True


def verify(game_data: GameData, fe_id: str) -> bool:
    return fe_id in game_data.financial_entities


def transfer_all(game_data: GameData, sender_fe_id: str, receiver_fe_id: str):
    if sender_fe_id in game_data.financial_entities and receiver_fe_id in game_data.financial_entities:
        sender_fe = game_data.financial_entities[sender_fe_id]
        receiver_fe = game_data.financial_entities[receiver_fe_id]
        t_plus = game_data.environment.time.get_t_plus_from_now()
        for currency_id, amount in sender_fe.wallet.currencies.items():
            if amount == 0:
                continue
            _pay(fe=sender_fe, currency_id=currency_id, amount=amount)
            _receive(fe=receiver_fe, currency_id=currency_id, amount=amount)
            _record(fe=sender_fe, target_fe_id=receiver_fe_id, target_fe=receiver_fe, currency_id=currency_id,
                    amount=-amount, success=True, t_plus=t_plus)
            _record(fe=receiver_fe, target_fe_id=sender_fe_id, target_fe=sender_fe, currency_id=currency_id,
                    amount=amount, success=True, t_plus=t_plus)


def transfer(game_data: GameData, sender_fe_id: str, receiver_fe_id: str, currency_id: str, amount: int) -> bool:
    success = False
    if sender_fe_id in game_data.financial_entities and receiver_fe_id in game_data.financial_entities:
        sender_fe = game_data.financial_entities[sender_fe_id]
        receiver_fe = game_data.financial_entities[receiver_fe_id]
        if _pay(fe=sender_fe, currency_id=currency_id, amount=amount):
            _receive(fe=receiver_fe, currency_id=currency_id, amount=amount)
            success = True
        else:
            success = False
        t_plus = game_data.environment.time.get_t_plus_from_now()
        # record for sender
        _record(fe=sender_fe, target_fe_id=receiver_fe_id, target_fe=receiver_fe, currency_id=currency_id,
                amount=-amount, success=success, t_plus=t_plus)
        # record for receiver
        if success:
            _record(fe=receiver_fe, target_fe_id=sender_fe_id, target_fe=sender_fe, currency_id=currency_id,
                    amount=amount, success=success, t_plus=t_plus)
    return success


def financial_count(game_data: GameData, fe_id: str, currency_id: str) -> int:
    fe = game_data.financial_entities[fe_id]
    if fe is None:
        return 0
    return _count(fe=fe, currency_id=currency_id)


def _count(fe: FinancialEntity, currency_id: str) -> int:
    return fe.wallet.currencies[currency_id] if currency_id in fe.wallet.currencies else 0


def _pay(fe: FinancialEntity, currency_id: str, amount: int) -> bool:
    if _count(fe=fe, currency_id=currency_id) >= amount:
        fe.wallet.currencies[currency_id] -= amount
        return True
    else:
        return False


def _receive(fe: FinancialEntity, currency_id: str, amount: int):
    if _count(fe=fe, currency_id=currency_id) == 0:
        fe.wallet.currencies[currency_id] = amount
    else:
        fe.wallet.currencies[currency_id] += amount


def _record(fe: FinancialEntity, target_fe_id: str, target_fe: FinancialEntity, currency_id: str, amount: int,
            success: bool, t_plus: int):
    fe.wallet.transactions.insert(0, Transaction(target_fe_id=target_fe_id, target_name=target_fe.name,
                                                 currency_id=currency_id, amount=amount,
                                                 success=success, t_plus=t_plus))
    if len(fe.wallet.transactions) > 100000:
        fe.wallet.transactions = fe.wallet.transactions[:100000]
