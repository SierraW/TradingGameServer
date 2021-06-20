from models.Wallet import Wallet


class FinancialEntity(object):
    def __init__(self, name: str, entity_type: int):
        self.name = name
        self.entity_type = entity_type
        self.wallet = Wallet()

    @staticmethod
    def from_dict(source):
        fe = FinancialEntity(source['name'], source['entity_type'])
        fe.wallet = Wallet.from_dict(source['wallet'])
        return fe

    def to_dict(self):
        return {
            'name': self.name,
            'entity_type': self.entity_type,
            'wallet': self.wallet.to_dict()
        }

    def __repr__(self):
        return f'Company(name={self.name}, wallet={self.wallet.to_dict()})'