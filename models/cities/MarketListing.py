
class MarketListing(object):
    def __init__(self, market_id, seller_fe_id, product_category: int, product_id, currency_id, amount, price_per_unit,
                 discount_rate: float, remaining_days: int, is_retail_sale: bool, original_storage_id: str):
        self.listing_id = None
        self.market_id = market_id
        self.seller_fe_id = seller_fe_id
        self.product_category = product_category
        self.product_id = product_id
        self.currency_id = currency_id
        self.amount = amount
        self.price_per_unit = price_per_unit
        self.discount_rate = discount_rate
        self.remaining_days = remaining_days
        self.is_retail_sale = is_retail_sale
        self.original_storage_id = original_storage_id

    @staticmethod
    def from_dict(source):
        listing = MarketListing(market_id=source['market_id'], seller_fe_id=source['seller_fe_id'],
                                product_id=source['product_id'], currency_id=source['currency_id'],
                                amount=source['amount'], product_category=source['product_category'],
                                price_per_unit=source['price_per_unit'],
                                discount_rate=source['discount_rate'],
                                is_retail_sale=source['is_retail_sale'],
                                remaining_days=source['remaining_days'],
                                original_storage_id=source['original_storage_id'])
        if 'auto_discount' in source:
            listing.auto_discount = source['auto_discount']
        return listing

    def to_dict(self):
        return {
            'market_id': self.market_id,
            'seller_fe_id': self.seller_fe_id,
            'product_category': self.product_category,
            'product_id': self.product_id,
            'currency_id': self.currency_id,
            'amount': self.amount,
            'price_per_unit': self.price_per_unit,
            'discount_rate': self.discount_rate,
            'remaining_days': self.remaining_days,
            'is_retail_sale': self.is_retail_sale,
            'original_storage_id': self.original_storage_id
        }

    def __repr__(self):
        return self.to_dict().__repr__()

    def get_discounted_price_per_unit(self) -> float:
        return self.price_per_unit * (1 - self.discount_rate)

    def get_final_price(self, amount: int = None) -> int:
        price = int(self.get_discounted_price_per_unit() * (amount if amount is not None else self.amount))
        return 1 if price < 1 else price
