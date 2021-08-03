from typing import Optional

import debug_toolkit
from controllers.financial_controller import transfer
from controllers.market_record_controller import get_previous_average_price, submit_receipt
from controllers.storage_controller import storage_remove_from_storage, storage_get_storage, storage_add_to_storage
from data import GameData
from models.cities.Market import Market
from models.cities.MarketListing import MarketListing
from models.cities.MarketReceipt import MarketPurchaseReceipt


def market_get_market(game_data: GameData, market_id: str) -> Market:
    return game_data.markets[market_id]


def market_get_market_listing(game_data: GameData, market_listing_id: str) -> MarketListing:
    return game_data.market_listings[market_listing_id]


def market_listings_loop(game_data: GameData):
    _debug_func_name = 'market_listings_loop'
    debug_toolkit.function_start(_debug_func_name)
    lids_to_be_remove = []
    for lid, market_listing in game_data.market_listings.items():
        if market_listing.remaining_days > 0:
            market_listing.remaining_days -= 1
        else:
            lids_to_be_remove.append(lid)
    for lid in lids_to_be_remove:
        market_unregister_market_listing(game_data=game_data, market_listing_id=lid)
        debug_toolkit.debug_print(_debug_func_name, 'deleting expired market listing', [lid])
        del game_data.market_listings[lid]
    debug_toolkit.function_end(_debug_func_name)


def market_get_recommended_pricing(game_data: GameData, market_id: str, product_id: str,
                                   recommended_price_per_unit: int, bottom_price_per_unit: int,
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
    return recommended_price_per_unit


def verify_financial_entity_retail_access(game_data: GameData, financial_id: str) -> bool:
    if financial_id in game_data.companies:
        company = game_data.companies[financial_id]
        if company.company_type == 1:
            return True
    return False


def market_register_product(game_data: GameData, market_id: str, seller_fe_id: str, product_id: str, amount: int,
                            currency_id: str, price_per_unit: int, is_retail_sale: bool, storage_id: str) -> bool:
    if product_id not in game_data.products:
        return False
    # verify access
    if is_retail_sale and not verify_financial_entity_retail_access(game_data=game_data, financial_id=seller_fe_id):
        print(f'Warning: This financial entity {seller_fe_id} has no access to retail market.')
        return False
    # verify storage_id
    market = market_get_market(game_data=game_data, market_id=market_id)
    if market.city_id != game_data.storages[storage_id].city_id:
        return False
    if not storage_remove_from_storage(game_data=game_data, products={product_id: amount}, storage_id=storage_id):
        return False

    product = game_data.products[product_id]
    listings = MarketListing(market_id=market_id, seller_fe_id=seller_fe_id, product_id=product_id,
                             currency_id=currency_id, amount=amount, price_per_unit=price_per_unit,
                             discount_rate=0.0,
                             remaining_days=15,
                             is_retail_sale=is_retail_sale,
                             product_category=product.category,
                             original_storage_id=storage_id)
    listings_id = game_data.generate_identifier()
    game_data.market_listings[listings_id] = listings
    return True


def market_unregister_market_listing(game_data: GameData, market_listing_id: str, requester_fe_id: str = None,
                                     return_destination_storage_id: str = None) -> bool:
    _debug_function_name = 'market_unregister_market_listing'
    debug_toolkit.function_start(_debug_function_name,
                                 [requester_fe_id, market_listing_id, return_destination_storage_id])
    if market_listing_id not in game_data.market_listings:
        debug_toolkit.warning_print(_debug_function_name, 'market_listing_id not found',
                                    [requester_fe_id, market_listing_id])
        return False
    market_listing = market_get_market_listing(game_data=game_data, market_listing_id=market_listing_id)
    if requester_fe_id is not None and market_listing.seller_fe_id != requester_fe_id:
        debug_toolkit.warning_print(_debug_function_name, 'access denied', [market_listing, requester_fe_id])
        return False
    if return_destination_storage_id is None:
        debug_toolkit.debug_print(_debug_function_name, 'Filling None value return_destination_storage_id', [market_listing.__repr__()])
        return_destination_storage_id = market_listing.original_storage_id
    if not storage_add_to_storage(game_data=game_data, products={market_listing.product_id: market_listing.amount},
                                  storage_id=return_destination_storage_id):
        return False
    debug_toolkit.function_end(_debug_function_name)
    return True


def _market_purchase_single_inner_city(game_data: GameData, listing: MarketListing, market: Market,
                                       buyer_fe_id: str, listing_id: str, amount: int,
                                       destination_storage_id: str, city_fe_id: str = None,
                                       tax_rate: float = None) -> Optional[MarketPurchaseReceipt]:
    # check the destination is in range
    if storage_get_storage(game_data=game_data, storage_id=destination_storage_id).city_id != market.city_id:
        print(f'Warning: This method is only for inner city purchase.')
        return None
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
        receipt = MarketPurchaseReceipt(market_id=listing.market_id, buyer_fe_id=buyer_fe_id, amount=amount,
                                        time=game_data.environment.time, listing_id=listing.listing_id,
                                        product_id=listing.product_id, currency_id=listing.currency_id,
                                        purchase_price=purchase_price, product_category=listing.product_category)
        submit_receipt(game_data=game_data, receipt=receipt)
        print(f'purchased {listing.product_id} at {purchase_price / amount}')
        # ship to buyer
        storage_add_to_storage(game_data=game_data, storage_id=destination_storage_id,
                               products={listing.product_id: amount})
        return receipt
    return None


def market_purchase_retail(game_data: GameData, buyer_fe_id: str, listing_id: str,
                           destination_storage_id: str, amount: int = None,
                           budget: int = None):
    if listing_id in game_data.market_listings:
        market_listing = game_data.market_listings[listing_id]
        if not market_listing.is_retail_sale:
            return None
        market = game_data.markets[market_listing.market_id]
        if amount is None:
            amount = market_listing.amount
        max_amount = int(budget / market_listing.price_per_unit) if budget is not None else market_listing.amount
        if max_amount < 1:
            return None
        if amount > max_amount:
            amount = max_amount
        if market_listing.amount < amount:
            amount = market_listing.amount
        if market.city_id is None or market.city_id not in game_data.cities:
            return _market_purchase_single_inner_city(game_data=game_data, listing=market_listing, market=market,
                                                      buyer_fe_id=buyer_fe_id, listing_id=listing_id, amount=amount,
                                                      destination_storage_id=destination_storage_id)
        else:
            city = game_data.cities[market.city_id]
            tax_rate = game_data.countries[city.country_id].tax_rate if city.country_id in game_data.countries else 0.0
            return _market_purchase_single_inner_city(game_data=game_data, listing=market_listing, market=market,
                                                      buyer_fe_id=buyer_fe_id, listing_id=listing_id, amount=amount,
                                                      city_fe_id=city.financial_id, tax_rate=tax_rate,
                                                      destination_storage_id=destination_storage_id)


def market_purchase_wholesale(game_data: GameData, buyer_fe_id: str, listing_id: str,
                              destination_storage_id: str):
    if listing_id in game_data.market_listings:
        market_listing = game_data.market_listings[listing_id]
        if market_listing.is_retail_sale:
            return None
        market = game_data.markets[market_listing.market_id]
        if market.city_id is None or market.city_id not in game_data.cities:
            return _market_purchase_single_inner_city(game_data=game_data, listing=market_listing, market=market,
                                                      buyer_fe_id=buyer_fe_id, listing_id=listing_id,
                                                      amount=market_listing.amount,
                                                      destination_storage_id=destination_storage_id)
        else:
            city = game_data.cities[market.city_id]
            tax_rate = game_data.countries[city.country_id].tax_rate if city.country_id in game_data.countries else 0.0
            return _market_purchase_single_inner_city(game_data=game_data, listing=market_listing, market=market,
                                                      buyer_fe_id=buyer_fe_id, listing_id=listing_id,
                                                      amount=market_listing.amount,
                                                      city_fe_id=city.financial_id, tax_rate=tax_rate,
                                                      destination_storage_id=destination_storage_id)


def market_get_market_listings(game_data: GameData, market_id: str, is_retail_sale: bool) -> list[MarketListing]:
    listings = []
    for lid, market_listing in game_data.market_listings.items():
        if market_id == market_listing.market_id and market_listing.is_retail_sale == is_retail_sale:
            market_listing.listing_id = lid
            listings.append(market_listing)
    return listings


def market_get_market_listings_by_category(game_data: GameData, market_id: str, is_retail_sale: bool, category: int,
                                           reverse: bool = False) -> list[MarketListing]:
    filtered_market_listings = filter(lambda market_listing: market_listing.product_category == category,
                                      market_get_market_listings(game_data=game_data,
                                                                 market_id=market_id,
                                                                 is_retail_sale=is_retail_sale))
    return list(sorted(filtered_market_listings,
                       key=lambda market_listing: market_listing.get_discounted_price_per_unit(), reverse=reverse))


def market_purchase_by_category(game_data: GameData, buyer_fe_id: str, category: int, amount_required: int,
                                market_id: str, available_budget: int,
                                destination_storage_id: str, listings: list = None) -> MarketPurchaseReceipt:
    budget = available_budget
    amount = amount_required
    if listings is None:
        listings = market_get_market_listings(game_data=game_data, market_id=market_id, is_retail_sale=True)
    listings.sort(key=lambda item: item.get_discounted_price_per_unit())
    purchased = 0
    for listing in listings:
        if amount == 0 or budget == 0 or listing.product_id not in game_data.products:
            break
        if listing.product_category == category:
            receipt = market_purchase_retail(game_data=game_data, buyer_fe_id=buyer_fe_id,
                                             listing_id=listing.listing_id, amount=amount, budget=budget,
                                             destination_storage_id=destination_storage_id)
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


def market_purchase(game_data: GameData, buyer_fe_id: str, products: dict, market_id: str, budget: int,
                    destination_storage_id: str,
                    listings: list = None) -> dict:
    if listings is None:
        listings = market_get_market_listings(game_data=game_data, market_id=market_id, is_retail_sale=True)
    listings.sort(key=lambda item: item.get_discounted_price_per_unit())
    purchased = dict()
    for listing in listings:
        if not products or budget == 0:
            return purchased
        if listing.product_id in products:
            receipt = market_purchase_retail(game_data=game_data, buyer_fe_id=buyer_fe_id,
                                             listing_id=listing.listing_id,
                                             amount=products[listing.product_id], budget=budget,
                                             destination_storage_id=destination_storage_id)
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


def market_get_lowest_listing_price_for_product(game_data: GameData, market_id: str, product_id: str):
    market_listings = filter(lambda market_listing: market_listing.product_id == product_id,
                             market_get_market_listings(game_data=game_data, market_id=market_id,
                                                        is_retail_sale=True))
    market_listings = sorted(market_listings,
                             key=lambda market_listing: market_listing.get_discounted_price_per_unit())
    if len(market_listings) > 0:
        return market_listings[0].get_discounted_price_per_unit()
