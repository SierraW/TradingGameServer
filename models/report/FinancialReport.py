from models.report.Transaction import Transaction


class FinancialReport(object):
    def __init__(self, report_period_start_t_plus: int, report_period_end_t_plus: int,
                 initial_wallet_info: dict,
                 final_wallet_info: dict,
                 transactions: list[Transaction]):
        self.report_period_start_t_plus = report_period_start_t_plus
        self.report_period_end_t_plus = report_period_end_t_plus
        self.initial_wallet_info = initial_wallet_info
        self.final_wallet_info = final_wallet_info
        self.gain_lost_info = {}
        for currency_id, amount in final_wallet_info.items():
            if currency_id in initial_wallet_info:
                self.gain_lost_info[currency_id] = amount - initial_wallet_info[currency_id]
            else:
                self.gain_lost_info[currency_id] = amount
        self.transactions = transactions
        self.failed_transactions = list(filter(lambda transaction: not transaction.success, self.transactions))
