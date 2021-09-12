from controllers.financial_controller import transfer
from controllers.population_controller import get_employee_salary
from models.GameData import GameData
from models.PropertyListing import PropertyListing
from models.cities.property.Property import Property


def property_get_property(game_data: GameData, prop_id: str) -> Property:
    return game_data.properties[prop_id]


def property_register_property_for_sale(game_data: GameData, prop_id: str, seller_fe_id: str, price: int = None,
                                        currency_id: str = None, target_buyer_fe_id: str = None):
    if prop_id not in game_data.properties:
        print('register property failed: property not existed')
        return
    prop = game_data.properties[prop_id]
    if prop.financial_id != seller_fe_id:
        print('register property failed: permission denied')
        return
    city = game_data.cities[prop.city_id]
    if currency_id is None:
        currency_id = city.currency_id
    if price is None:
        price = int(city.land_tax_rate * get_employee_salary(population=city.population))
    prop_listing = PropertyListing(city_id=prop.city_id, property_id=prop_id, currency_id=currency_id, price=price,
                                   target_buyer_fe_id=target_buyer_fe_id)
    pl_id = game_data.generate_identifier()
    game_data.property_listings[pl_id] = prop_listing
    return pl_id


def get_properties_by_city(game_data: GameData, city_id: str) -> dict:
    fetch_result = dict()
    for prop_id, prop in game_data.properties.items():
        if prop.city_id == city_id:
            fetch_result[prop_id] = prop
    return fetch_result


def get_property_listings(game_data: GameData, city_id: str) -> dict:
    fetch_result = dict()
    for pl_id, pl in game_data.property_listings.items():
        if pl.city_id == city_id:
            fetch_result[pl_id] = pl
    return fetch_result


def property_purchase_property(game_data: GameData, prop_listing_id: str, buyer_fe_id: str) -> bool:
    if prop_listing_id not in game_data.property_listings:
        print('market_purchase failed: cannot find property listing')
        return False
    prop_listing = game_data.property_listings[prop_listing_id]
    prop = game_data.properties[prop_listing.property_id]
    if prop_listing.target_buyer_fe_id is not None and prop_listing.target_buyer_fe_id != buyer_fe_id:
        print('market_purchase failed: permission denied')
        return False
    if transfer(game_data=game_data, sender_fe_id=buyer_fe_id, receiver_fe_id=prop.financial_id,
                currency_id=prop_listing.currency_id, amount=prop_listing.price):
        prop.financial_id = buyer_fe_id
        property_remove_task(prop=prop)
        del game_data.property_listings[prop_listing_id]
        return True
    return False


def property_remove_task(prop: Property):
    prop.production = None
    prop.auto_register_market_id = None
    prop.auto_managed = False


def property_generate_property(game_data: GameData, city_id: str, serial_name: str, name: str):
    prop_id = game_data.generate_identifier()
    game_data.properties[prop_id] = Property(city_id=city_id,
                                             serial_name=serial_name,
                                             name=name,
                                             financial_id=city_id,
                                             size=3)
    return prop_id
