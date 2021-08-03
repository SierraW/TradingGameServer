import copy
from typing import Optional

import debug_toolkit
from controllers.financial_controller import financial_get_financial_entity
from models.GameData import GameData
from models.report.FinancialReport import FinancialReport
from models.report.Transaction import Transaction


def financial_report_get_yearly_report(game_data: GameData, financial_id: str, year: int) -> Optional[FinancialReport]:
    current_year = game_data.environment.time.year
    if year < 0:
        if current_year + year < 0:
            return None
        else:
            return financial_report_get_yearly_report(game_data=game_data, financial_id=financial_id,
                                                      year=current_year + year)
    else:
        if year > current_year:
            return None
        period = game_data.environment.time.get_t_plus_period_for_year(year=year)
        return financial_report_generate_periodic_report(game_data=game_data, financial_id=financial_id,
                                                         start_t_plus=period[0], end_t_plus=period[1])


def _calculate_balance(current_balance: dict, transactions: list[Transaction]) -> dict:
    new_balance = copy.deepcopy(current_balance)
    for transaction in transactions:
        new_balance[transaction.currency_id] += transaction.amount
    return new_balance


def financial_report_generate_periodic_report(game_data: GameData, financial_id: str, start_t_plus: int,
                                              end_t_plus: int) -> Optional[FinancialReport]:
    _debug_func_name = 'financial_report_generate_periodic_report'
    debug_toolkit.function_start(_debug_func_name, [financial_id, start_t_plus, end_t_plus])

    if financial_id not in game_data.financial_entities:
        debug_toolkit.warning_print(_debug_func_name, 'Financial ID not exist', [financial_id])
        return None
    fe = financial_get_financial_entity(game_data=game_data, financial_id=financial_id)
    transactions_till_end = list(filter(lambda transaction: transaction.t_plus > end_t_plus,
                                        fe.wallet.transactions))
    transactions_in_period = list(filter(lambda transaction: start_t_plus <= transaction.t_plus <= end_t_plus,
                                         fe.wallet.transactions))
    end_wallet = _calculate_balance(current_balance=fe.wallet.currencies, transactions=transactions_till_end)
    start_wallet = _calculate_balance(current_balance=end_wallet, transactions=transactions_in_period)
    debug_toolkit.debug_print(_debug_func_name, args=[start_wallet, end_wallet])
    debug_toolkit.function_end(_debug_func_name)
    return FinancialReport(report_period_start_t_plus=start_t_plus, report_period_end_t_plus=end_t_plus,
                           initial_wallet_info=start_wallet, final_wallet_info=end_wallet,
                           transactions=transactions_in_period)
