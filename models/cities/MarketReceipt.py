from models.TGTime import TGTime
from models.cities.Market import Market
from models.cities.MarketListing import MarketListing


class MarketPurchaseReceipt(object):
    def __init__(self, market: Market, listing: MarketListing, buyer_fe_id: str, amount: int, time: TGTime):
        self.market_id = market.market_id
        self.market_name = market.name
        self.listing_id = listing.listing_id
        self.product_id = listing.product_id
        self.buyer_id = buyer_fe_id
        self.amount = amount
        self.total_price = amount * listing.price_per_unit
        self.t_plus = time.get_t_plus_from_now()

