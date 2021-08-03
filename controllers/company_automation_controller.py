from controllers.financial_controller import financial_count
from controllers.market_controller import market_get_market_listings_by_category, market_purchase_wholesale, \
    market_register_product
from controllers.property_controller import get_property_listings, property_purchase_property, property_get_property
from controllers.storage_controller import storage_check_storage_by_type, storage_get_products_by_category
from models.Company import Company
from models.GameData import GameData


def type_0_company_automation(game_data: GameData, company: Company, property_dict: dict):
    if len(property_dict) == 0:
        minimum_price_pl_id = None
        minimum_price = None
        for pl_id, property_listing in get_property_listings(game_data=game_data, city_id=company.city_id).items():
            if minimum_price is None or property_listing.price < minimum_price:
                minimum_price = property_listing.price
                minimum_price_pl_id = pl_id
        if minimum_price is not None and minimum_price_pl_id is not None:
            property_purchase_property(game_data=game_data, prop_listing_id=minimum_price_pl_id,
                                       buyer_fe_id=company.financial_id)


def type_1_company_automation(game_data: GameData, company: Company):  # food retailer
    if not company.auto_managed:
        return
    if company.property_id is None:
        print(f'Warning: Automation failed at company {company.financial_id}')
        return

    reminder_avg_price_string = "avg_price"

    def get_average_price() -> float:
        return company.reminder[reminder_avg_price_string] if reminder_avg_price_string in company.reminder \
            else 0.0

    def record_average_price(old_amount: int, old_price: float, amount_purchased: int, whole_price: int) \
            -> float:
        combined_price = old_amount * old_price + whole_price
        new_avg_price = combined_price / (old_amount + amount_purchased)
        company.reminder[reminder_avg_price_string] = new_avg_price
        return new_avg_price

    city = game_data.cities[company.city_id]
    company_property = property_get_property(game_data=game_data, prop_id=company.property_id)

    population_size = len(city.population.humans)
    product_size = storage_check_storage_by_type(game_data=game_data, category=0,
                                                 storage_id=company_property.storage_id)

    prefer_size = population_size * 120
    regular_size = population_size * 60
    minimum_required_size = population_size * 30
    fund = financial_count(game_data=game_data, fe_id=company.financial_id, currency_id=city.currency_id)

    # market_purchase phase
    def purchase_market_listing(current_amount: int, current_avg_price: float, listing_id: str) -> tuple[float, int]:
        receipt = market_purchase_wholesale(game_data=game_data, buyer_fe_id=company.financial_id,
                                            listing_id=listing_id, destination_storage_id=company_property.storage_id)
        if receipt is not None:
            temp_avg_price = record_average_price(old_amount=current_amount, old_price=current_avg_price,
                                                  amount_purchased=receipt.amount,
                                                  whole_price=receipt.total_price)
            final_product_size = receipt.amount + current_amount
            return temp_avg_price, final_product_size

    print(f'Purchase phase fund {fund}, product_size {product_size}, prefer_size {prefer_size}')
    if fund > 100 and product_size < prefer_size:
        whole_sell_listings = market_get_market_listings_by_category(game_data=game_data, market_id=city.market_id,
                                                                     is_retail_sale=False, category=0)
        print(whole_sell_listings)
        if len(whole_sell_listings) > 0:
            avg_price = get_average_price()
            while product_size < prefer_size and len(whole_sell_listings) > 0:
                market_listing = whole_sell_listings[0]
                if market_listing.price_per_unit <= avg_price:
                    print(f'buy it!')
                    purchase_result = purchase_market_listing(current_amount=product_size, current_avg_price=avg_price,
                                                              listing_id=market_listing.listing_id)
                    if purchase_result is not None:
                        avg_price = purchase_result[0]
                        product_size = purchase_result[1]
                elif market_listing.price_per_unit < avg_price * 1.1 and product_size < regular_size:
                    print(f'buy it?')
                    purchase_result = purchase_market_listing(current_amount=product_size, current_avg_price=avg_price,
                                                              listing_id=market_listing.listing_id)
                    if purchase_result is not None:
                        avg_price = purchase_result[0]
                        product_size = purchase_result[1]
                elif product_size < minimum_required_size:
                    print(f'I dont want to but i have to')
                    purchase_result = purchase_market_listing(current_amount=product_size, current_avg_price=avg_price,
                                                              listing_id=market_listing.listing_id)
                    if purchase_result is not None:
                        avg_price = purchase_result[0]
                        product_size = purchase_result[1]

    # sell phase
    avg_price = get_average_price()
    if product_size == 0 or avg_price < 0.01:
        return
    retail_listings = market_get_market_listings_by_category(game_data=game_data, market_id=city.market_id,
                                                             is_retail_sale=True, category=0)

    def register_for_sell(amount: int, price_per_unit: int):
        amount_to_sell = amount
        products_to_sell = storage_get_products_by_category(game_data=game_data, storage_id=company_property.storage_id,
                                                            category=0)
        for pid, amount in products_to_sell.items():
            if amount > amount_to_sell:
                amount = amount_to_sell
            if market_register_product(game_data=game_data, market_id=city.market_id, seller_fe_id=company.financial_id,
                                       product_id=pid, amount=amount, currency_id=city.currency_id,
                                       price_per_unit=price_per_unit, is_retail_sale=True,
                                       storage_id=company_property.storage_id):
                amount_to_sell -= amount
            if amount_to_sell == 0:
                break

    if len(retail_listings) > 0:
        listed_amount = 0
        total_price_at_listings = 0
        for market_listing in retail_listings:
            listed_amount += market_listing.amount
            total_price_at_listings += market_listing.price_per_unit * market_listing.amount
        avg_price_at_listing = total_price_at_listings / listed_amount if listed_amount != 0 else 0.0
        if listed_amount < population_size:
            register_for_sell(amount=population_size - listed_amount, price_per_unit=int(avg_price * 1.2))
        elif avg_price * 1.1 < avg_price_at_listing:
            register_for_sell(amount=int(population_size / 3), price_per_unit=int(avg_price * 1.1))
    else:
        register_for_sell(amount=population_size, price_per_unit=int(avg_price * 1.2))
