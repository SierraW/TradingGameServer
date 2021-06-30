from controllers.financial_controller import transfer
from data import GameData
from models.cities.City import City
from models.cities.Market import Market
from models.cities.MarketListing import MarketListing
from models.cities.MarketReceipt import MarketPurchaseReceipt
from controllers.market_record_controller import get_previous_average_price


def market_listings_loop(game_data: GameData):
    for _, market_listing in game_data.market_listings.items():
        if market_listing.auto_discount and market_listing.discount_rate < 0.9:
            market_listing.discount_rate += 0.05

def calculate_shared_price(market: Market, purchase_price: int) -> int:
    return int(purchase_price * market.handling_fee_rate)


def register_market_listing(game_data: GameData, market_id: str, seller_fe_id: str, product_id: str, amount: int,
                            price_per_unit: int = None, currency_id: str = None):
    auto_register = False
    if currency_id is None:
        market = game_data.markets[market_id]
        currency_id = market.currency_id
    if price_per_unit is None:
        price_per_unit = get_previous_average_price(game_data=game_data, market_id=market_id, product_id=product_id,
                                                    currency_id=currency_id)
        price_per_unit = int(price_per_unit * 1.1)
        auto_register = True
    listings = MarketListing(market_id=market_id, seller_fe_id=seller_fe_id, product_id=product_id,
                             currency_id=currency_id, amount=amount, price_per_unit=price_per_unit,
                             auto_discount=auto_register, discount_rate=0.0)
    if auto_register:
        listings.auto_discount = True
    listings_id = game_data.generate_identifier()
    game_data.market_listings[listings_id] = listings


def purchase_single(game_data: GameData, buyer_fe_id: str, listing_id: str, amount: int = None,
                    budget: int = None) -> MarketPurchaseReceipt:
    if listing_id in game_data.market_listings:
        listing = game_data.market_listings[listing_id]
        market = game_data.markets[listing.market_id]
        if amount is None:
            amount = listing.amount
        max_amount = budget / listing.price_per_unit
        if amount > max_amount:
            amount = max_amount
        if listing.amount < amount:
            amount = listing.amount
        purchase_price = listing.get_final_price(amount=amount)
        handling_fee = calculate_shared_price(market=market, purchase_price=purchase_price)
        # transfer to market
        if transfer(game_data=game_data, sender_fe_id=buyer_fe_id, receiver_fe_id=market.financial_id,
                    currency_id=listing.currency_id, amount=purchase_price):
            listing.amount -= amount
            if listing.amount == 0:
                del game_data.market_listings[listing_id]
            # todo: update_listing(game_data=game_data, listing_id=listing_id)
            # transfer to seller
            transfer(game_data=game_data, sender_fe_id=market.financial_id, receiver_fe_id=listing.seller_fe_id,
                     currency_id=listing.currency_id, amount=purchase_price - handling_fee)
            return MarketPurchaseReceipt(market=market, listing=listing, buyer_fe_id=buyer_fe_id, amount=amount,
                                         time=game_data.environment.time)


def purchase(game_data: GameData, buyer_fe_id: str, products: dict, city: City, budget: int, listings: list = None) \
        -> dict:
    if listings is None:
        listings = []
        market_id = city.market_id
        for lid, listing in game_data.market_listings.items():
            if market_id is listing.market_id:
                listing.listing_id = lid
                listings.append(listing)
    listings.sort(key=lambda item: item.get_discounted_price_per_unit())
    purchased = dict()
    for listing in listings:
        if listing.product_id in products:
            receipt = purchase_single(game_data=game_data, buyer_fe_id=buyer_fe_id,
                                      listing_id=listing.listing_id,
                                      amount=products[listing.product_id],
                                      budget=budget)
            if receipt is not None:
                if purchased[listing.product_id] is None:
                    purchased[listing.product_id] = 0
                purchased[listing.product_id] += receipt.amount
                budget -= receipt.total_price
                products[listing.product_id] -= receipt.amount
                if products[listing.product_id] == 0:
                    del products[listing.product_id]
    return purchased
