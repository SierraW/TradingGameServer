class MarketListing(object):
    def __init__(self, market_id, seller_fe_id, product_id, currency_id, amount, price_per_unit):
        self.market_id = market_id
        self.seller_fe_id = seller_fe_id
        self.product_id = product_id
        self.currency_id = currency_id
        self.amount = amount
        self.price_per_unit = price_per_unit

    @staticmethod
    def from_dict(source):
        return MarketListing(market_id=source['market_id'], seller_fe_id=source['seller_fe_id'],
                             product_id=source['product_id'], currency_id=source['currency_id'],
                             amount=source['amount'],
                             price_per_unit=source['price_per_unit'])

    def to_dict(self):
        return {
            'market_id': self.market_id,
            'seller_fe_id': self.seller_fe_id,
            'product_id': self.product_id,
            'currency_id': self.currency_id,
            'amount': self.amount,
            'price_per_unit': self.price_per_unit
        }
