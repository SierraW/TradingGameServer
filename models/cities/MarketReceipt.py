from models.TGTime import TGTime
from models.cities.Market import Market
from models.cities.MarketListing import MarketListing


class MarketPurchaseReceipt(object):
    def __init__(self, market_id: str, listing_id: str, product_category: int, product_id: str, buyer_fe_id: str,
                 currency_id: str, purchase_price: int, amount: int, time: TGTime):
        self.market_id = market_id
        self.listing_id = listing_id
        self.product_id = product_id
        self.product_category = product_category
        self.buyer_fe_id = buyer_fe_id
        self.amount = amount
        self.currency_id = currency_id
        self.total_price = purchase_price
        self.t_plus = time.get_t_plus_from_now()

    def to_dict(self):
        return {
            'type': 'market_receipt',
            'market_id': self.market_id,
            'listing_id': self.listing_id,
            'product_id': self.product_id,
            'product_category': self.product_category,
            'buyer_fe_id': self.buyer_fe_id,
            'amount': self.amount,
            'currency_id': self.currency_id,
            'total_price': self.total_price,
            't_plus': self.t_plus
        }

    def __repr__(self):
        return self.to_dict().__repr__()
