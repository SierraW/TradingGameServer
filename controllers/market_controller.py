from controllers.financial_controller import transfer
from data import GameData
from models.cities.Market import Market
from models.cities.MarketListing import MarketListing
from models.cities.MarketReceipt import MarketPurchaseReceipt
from controllers.market_record_controller import get_previous_average_price, submit_receipt


def market_listings_loop(game_data: GameData):
    for _, market_listing in game_data.market_listings.items():
        if market_listing.auto_discount is not None and market_listing.discount_rate < 0.9:
            if market_listing.auto_discount > 0:
                market_listing.auto_discount -= 1
            else:
                market_listing.discount_rate += 0.05


def auto_register_market_listing(game_data: GameData, market_id: str, seller_fe_id: str, product_id: str, amount: int,
                                 recommended_price_per_unit: int, bottom_price_per_unit: int, auto_register: bool,
                                 currency_id: str = None):
    if currency_id is None:
        market = game_data.markets[market_id]
        currency_id = market.currency_id
    price = get_previous_average_price(game_data=game_data, market_id=market_id, product_id=product_id,
                                       currency_id=currency_id)
    if price is not None:
        if price > recommended_price_per_unit:
            recommended_price_per_unit = price
        elif price < bottom_price_per_unit:
            recommended_price_per_unit = bottom_price_per_unit
    return register_market_listing(game_data=game_data, market_id=market_id, seller_fe_id=seller_fe_id,
                                   product_id=product_id, amount=amount, currency_id=currency_id,
                                   price_per_unit=recommended_price_per_unit, auto_register=auto_register)


def register_market_listing(game_data: GameData, market_id: str, seller_fe_id: str, product_id: str, amount: int,
                            currency_id: str, price_per_unit: int, auto_register: bool) -> bool:
    if product_id not in game_data.products:
        return False
    product = game_data.products[product_id]
    listings = MarketListing(market_id=market_id, seller_fe_id=seller_fe_id, product_id=product_id,
                             currency_id=currency_id, amount=amount, price_per_unit=price_per_unit,
                             auto_discount=3 if auto_register else None, discount_rate=0.0,
                             product_category=product.category)
    if auto_register:
        listings.auto_discount = True
    listings_id = game_data.generate_identifier()
    game_data.market_listings[listings_id] = listings
    return True


def _purchase_single(game_data: GameData, listing: MarketListing, market: Market,
                     buyer_fe_id: str, listing_id: str, amount: int, city_fe_id: str = None, tax_rate: float = None):
    purchase_price = listing.get_final_price(amount=amount)
    tax = int(purchase_price * tax_rate) if tax_rate is not None else 0
    handling_fee = int((purchase_price - tax) * market.handling_fee_rate)
    # transfer to market
    if transfer(game_data=game_data, sender_fe_id=buyer_fe_id, receiver_fe_id=market.financial_id,
                currency_id=listing.currency_id, amount=purchase_price):
        listing.amount -= amount
        if listing.amount == 0:
            del game_data.market_listings[listing_id]
        # todo: update_listing(game_data=game_data, listing_id=listing_id)
        # transfer to heidal_city
        if city_fe_id is not None:
            transfer(game_data=game_data, sender_fe_id=market.financial_id, receiver_fe_id=city_fe_id,
                     currency_id=listing.currency_id, amount=tax)
        # transfer to seller
        transfer(game_data=game_data, sender_fe_id=market.financial_id, receiver_fe_id=listing.seller_fe_id,
                 currency_id=listing.currency_id, amount=purchase_price - tax - handling_fee)
        receipt = MarketPurchaseReceipt(market_id=market.market_id, buyer_fe_id=buyer_fe_id, amount=amount,
                                        time=game_data.environment.time, listing_id=listing.listing_id,
                                        product_id=listing.product_id, currency_id=listing.currency_id,
                                        purchase_price=purchase_price, product_category=listing.product_category)
        submit_receipt(game_data=game_data, receipt=receipt)
        print(f'purchased {listing.product_id} at {purchase_price / amount}')
        return receipt


def purchase_single(game_data: GameData, buyer_fe_id: str, listing_id: str, amount: int = None,
                    budget: int = None):
    if listing_id in game_data.market_listings:
        listing = game_data.market_listings[listing_id]
        market = game_data.markets[listing.market_id]
        if amount is None:
            amount = listing.amount
        max_amount = int(budget / listing.price_per_unit) if budget is not None else listing.amount
        if max_amount < 1:
            return None
        if amount > max_amount:
            amount = max_amount
        if listing.amount < amount:
            amount = listing.amount
        if market.city_id is None or market.city_id not in game_data.cities:
            return _purchase_single(game_data=game_data, listing=listing, market=market,
                                    buyer_fe_id=buyer_fe_id, listing_id=listing_id, amount=amount)
        else:
            city = game_data.cities[market.city_id]
            tax_rate = game_data.countries[city.country_id].tax_rate if city.country_id in game_data.countries else 0.0
            return _purchase_single(game_data=game_data, listing=listing, market=market,
                                    buyer_fe_id=buyer_fe_id, listing_id=listing_id, amount=amount,
                                    city_fe_id=city.financial_id, tax_rate=tax_rate)


def get_market_listings_by_market_id(game_data: GameData, market_id: str) -> list[MarketListing]:
    listings = []
    for lid, listing in game_data.market_listings.items():
        if market_id is listing.market_id:
            listing.listing_id = lid
            listings.append(listing)
    return listings


def purchase_by_category(game_data: GameData, buyer_fe_id: str, category: int, amount_required: int,
                         market_id: str, available_budget: int, listings: list = None) -> MarketPurchaseReceipt:
    budget = available_budget
    amount = amount_required
    if listings is None:
        listings = get_market_listings_by_market_id(game_data=game_data, market_id=market_id)
    listings.sort(key=lambda item: item.get_discounted_price_per_unit())
    purchased = 0
    for listing in listings:
        if amount == 0 or budget == 0 or listing.product_id not in game_data.products:
            break
        product = game_data.products[listing.product_id]
        if product.category == category:
            receipt = purchase_single(game_data=game_data, buyer_fe_id=buyer_fe_id,
                                      listing_id=listing.listing_id,
                                      amount=amount,
                                      budget=budget)
            if receipt is not None:
                purchased += receipt.amount
                budget -= receipt.total_price
                amount -= receipt.amount
            else:
                break
    return MarketPurchaseReceipt(market_id=market_id, buyer_fe_id=buyer_fe_id, amount=amount_required - amount,
                                 time=game_data.environment.time, listing_id="None",
                                 product_id="None", product_category=category,
                                 currency_id="N/A", purchase_price=available_budget - budget)


def purchase(game_data: GameData, buyer_fe_id: str, products: dict, market_id: str, budget: int,
             listings: list = None) -> dict:
    if listings is None:
        listings = get_market_listings_by_market_id(game_data=game_data, market_id=market_id)
    listings.sort(key=lambda item: item.get_discounted_price_per_unit())
    purchased = dict()
    for listing in listings:
        if not products or budget == 0:
            return purchased
        if listing.product_id in products:
            receipt = purchase_single(game_data=game_data, buyer_fe_id=buyer_fe_id,
                                      listing_id=listing.listing_id,
                                      amount=products[listing.product_id],
                                      budget=budget)
            if receipt is not None:
                if listing.product_id not in purchased:
                    purchased[listing.product_id] = 0
                purchased[listing.product_id] += receipt.amount
                budget -= receipt.total_price
                products[listing.product_id] -= receipt.amount
                if products[listing.product_id] == 0:
                    del products[listing.product_id]
            else:
                del products[listing.product_id]
    return purchased


def get_lowest_listing_price_for_product(game_data: GameData, market_id: str, product_id: str):
    market_listings = filter(lambda market_listing: market_listing.product_id == product_id,
                             get_market_listings_by_market_id(game_data=game_data, market_id=market_id))
    market_listings = sorted(market_listings,
                             key=lambda market_listing: market_listing.get_discounted_price_per_unit())
    if len(market_listings) > 0:
        return market_listings[0].get_discounted_price_per_unit()

