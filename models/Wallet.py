class Wallet(object):
    def __init__(self):
        self.currencies = dict()

    @staticmethod
    def from_dict(source):
        wallet = Wallet()
        wallet.currencies = source['wallet']
        return wallet

    def to_dict(self):
        return self.currencies

    def __repr__(self):
        return self.currencies.__repr__()

    def check(self, currency_id) -> int:
        return self.currencies[currency_id] if self.currencies[currency_id] is not None else 0

    def pay(self, currency_id, amount) -> bool:
        if self.check(currency_id=currency_id) >= amount:
            self.currencies[currency_id] -= amount
            return True
        else:
            return False

    def receive(self, currency_id, amount):
        if self.currencies[currency_id] is None:
            self.currencies[currency_id] = amount
        else:
            self.currencies[currency_id] += amount
