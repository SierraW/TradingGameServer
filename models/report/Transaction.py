class Transaction(object):
    def __init__(self, target_fe_id: str, target_name: str, currency_id: str, amount: int, success: bool,
                 t_plus: int):
        self.target_fe_id = target_fe_id
        self.target_name = target_name
        self.currency_id = currency_id
        self.amount = amount
        self.success = success
        self.t_plus = t_plus
