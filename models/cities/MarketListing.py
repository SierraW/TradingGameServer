from models.Buff import Buff


class MarketListing(object):
    def __init__(self, market_id, seller_fe_id, product_id, currency_id, amount, price_per_unit,
                 discount_rate: float, auto_discount: bool):
        self.listing_id = None
        self.market_id = market_id
        self.seller_fe_id = seller_fe_id
        self.product_id = product_id
        self.currency_id = currency_id
        self.amount = amount
        self.price_per_unit = price_per_unit
        self.discount_rate = discount_rate
        self.auto_discount = auto_discount

    @staticmethod
    def from_dict(source):
        listing = MarketListing(market_id=source['market_id'], seller_fe_id=source['seller_fe_id'],
                                product_id=source['product_id'], currency_id=source['currency_id'],
                                amount=source['amount'],
                                price_per_unit=source['price_per_unit'],
                                discount_rate=source['discount_rate'],
                                auto_discount=source['auto_discount'])
        return listing

    def to_dict(self):
        return {
            'market_id': self.market_id,
            'seller_fe_id': self.seller_fe_id,
            'product_id': self.product_id,
            'currency_id': self.currency_id,
            'amount': self.amount,
            'price_per_unit': self.price_per_unit,
            'discount_rate': self.discount_rate,
            'auto_discount': self.auto_discount
        }

    def get_discounted_price_per_unit(self) -> float:
        return self.price_per_unit * (1 - self.discount_rate)

    def get_final_price(self, amount: int) -> int:
        price = int(self.get_discounted_price_per_unit() * amount)
        return 1 if price < 1 else price
