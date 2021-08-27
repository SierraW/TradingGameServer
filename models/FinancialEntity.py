from models.StockWallet import StockWallet
from models.Wallet import Wallet


class FinancialEntity(object):
    def __init__(self, name: str, entity_type: int, currency_dict: dict = None):
        self.name = name
        self.entity_type = entity_type
        self.wallet = Wallet()
        if currency_dict is not None:
            self.wallet.currencies = currency_dict
        self.stock_wallet = StockWallet()

    @staticmethod
    def from_dict(source):
        fe = FinancialEntity(source['name'], source['entity_type'])
        fe.wallet = Wallet.from_dict(source['wallet'])
        fe.stock_wallet = StockWallet.from_dict(source['company_stock_dict'])
        return fe

    def to_dict(self):
        return {
            'name': self.name,
            'entity_type': self.entity_type,
            'wallet': self.wallet.to_dict(),
            'company_stock_dict': self.stock_wallet.to_dict()
        }

    def __repr__(self):
        return f'Company(name={self.name}, wallet={self.wallet.to_dict()})'