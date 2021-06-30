class Wallet(object):
    def __init__(self):
        self.currencies = dict()
        self.transactions = []

    @staticmethod
    def from_dict(source):
        wallet = Wallet()
        wallet.currencies = source['currencies']
        wallet.transactions = source['transactions']
        return wallet

    def to_dict(self):
        return {
            'currencies': self.currencies,
            'transactions': self.transactions
        }

    def __repr__(self):
        return self.currencies.__repr__()
