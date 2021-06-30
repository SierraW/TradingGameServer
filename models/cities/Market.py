class Market(object):
    def __init__(self, market_id, financial_id, storage_id, name, currency_id: str, handling_fee_rate):
        self.financial_id = financial_id
        self.market_id = market_id
        self.storage_id = storage_id
        self.name = name
        self.currency_id = currency_id
        self.handling_fee_rate = handling_fee_rate

    @staticmethod
    def from_dict(source):
        market = Market(market_id=source['market_id'], financial_id=source['financial_id'],
                        storage_id=source['storage_id'], name=source['name'], currency_id=source['currency_id'],
                        handling_fee_rate=source['handling_fee_rate'])
        return market

    def to_dict(self):
        return {
            'market_id': self.market_id,
            'financial_id': self.financial_id,
            'storage_id': self.storage_id,
            'name': self.name,
            'currency_id': self.currency_id,
            'handling_fee_rate': self.handling_fee_rate
        }
