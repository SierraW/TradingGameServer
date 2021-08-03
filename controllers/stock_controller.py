from controllers.financial_controller import financial_get_financial_entity
from models.GameData import GameData


def stock_arrange_initial_stock(game_data: GameData, company_id: str, initial_stock_distribution: dict):
    for fe_id, stock in initial_stock_distribution.items():
        fe = financial_get_financial_entity(game_data=game_data, financial_id=fe_id)
        fe.stock_wallet.company_stock_dict[company_id] = stock
