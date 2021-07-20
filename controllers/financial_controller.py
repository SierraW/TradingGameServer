from data import GameData
from models.FinancialEntity import FinancialEntity
from models.cities.Population import Population


def get_population_fe_id(population: Population, level: int) -> str:
    return population.fe_accounts[level]


def get_financial_entity(game_data: GameData, fe_id: str) -> FinancialEntity:
    return game_data.financial_entities[fe_id]


def register_financial_entity(game_data: GameData, name: str, entity_type: int) -> str:
    fe = FinancialEntity(name=name, entity_type=entity_type)
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


def transfer(game_data: GameData, sender_fe_id: str, receiver_fe_id: str, currency_id, amount) -> bool:
    success = False
    if sender_fe_id in game_data.financial_entities and receiver_fe_id in game_data.financial_entities:
        sender_fe = game_data.financial_entities[sender_fe_id]
        receiver_fe = game_data.financial_entities[receiver_fe_id]
        if _pay(fe=sender_fe, currency_id=currency_id, amount=amount):
            _receive(fe=receiver_fe, sender_fe_id=sender_fe_id, currency_id=currency_id, amount=amount)
            success = True
        else:
            success = False
        t_plus = game_data.environment.time.get_t_plus_from_now()
        # record for sender
        if success:
            _record(fe=sender_fe, target_fe_id=receiver_fe_id, target_fe=receiver_fe, currency_id=currency_id,
                    amount=-amount, t_plus=t_plus)
        else:
            _record(fe=sender_fe, target_fe_id=receiver_fe_id, target_fe=receiver_fe, currency_id=currency_id,
                    amount=-amount, t_plus=t_plus)
            _record(fe=sender_fe, target_fe_id=receiver_fe_id, target_fe=receiver_fe, currency_id=currency_id,
                    amount=amount, t_plus=t_plus)
        # record for receiver
        if success:
            _record(fe=receiver_fe, target_fe_id=sender_fe_id, target_fe=sender_fe, currency_id=currency_id,
                    amount=amount, t_plus=t_plus)
    return success


def count(game_data: GameData, fe_id: str, currency_id: str) -> int:
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


def _receive(fe: FinancialEntity, sender_fe_id: str, currency_id: str, amount: int):
    if _count(fe=fe, currency_id=currency_id) == 0:
        fe.wallet.currencies[currency_id] = amount
    else:
        fe.wallet.currencies[currency_id] += amount


def _record(fe: FinancialEntity, target_fe_id: str, target_fe: FinancialEntity, currency_id: str, amount: int,
            t_plus: int):
    fe.wallet.transactions.insert(0, {
        'target_fe_id': target_fe_id,
        'target_name': target_fe.name,
        'currency_id': currency_id,
        'amount': amount,
        't_plus': t_plus
    })
    if len(fe.wallet.transactions) > 100:
        fe.wallet.transactions = fe.wallet.transactions[:100]
