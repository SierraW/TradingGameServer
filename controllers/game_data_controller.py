from models.GameData import GameData
from database import *
from models.TGTime import TGTime


def register_market_listing(game_data: GameData, market_listing) -> str:
    ml_id = game_data.generate_identifier()
    game_data.market_listings[ml_id] = market_listing  # todo: replaced with auto update
    db_market_listings_ref.document(ml_id).set(market_listing.to_dict())
    return ml_id

def from_cloud(game_id: str) -> GameData:
    game_data = GameData()
    game_data.identifier = game_id
    time_doc = get_db(game_id, environment).document('time').get()
    if time_doc.exists:
        game_data.environment.time = TGTime.from_dict(time_doc.to_dict())

    return game_data


def backup():
    pass


def to_cloud(game_data: GameData):
    db_time_ref.set(game_data.environment.time.to_dict())
    db_identifier_factory_ref.set({'0': game_data.environment.identifier_factory})
    for entity_key in game_data.financial_entities:
        db_financial_entities_ref.document(entity_key).set(game_data.financial_entities[entity_key].to_dict())
    for storage_key in game_data.storages:
        db_storages_ref.document(storage_key).set(game_data.storages[storage_key].to_dict())
    for country_key, country in game_data.countries.items():
        db_countries_ref.document(country_key).set(country.to_dict())
    for city_key in game_data.cities:
        db_cities_ref.document(city_key).set(game_data.cities[city_key].to_dict())
    for market_key in game_data.markets:
        get_db(game_data.identifier, markets).document(market_key).set(game_data.markets[market_key].to_dict())
    for company_key, company in game_data.companies.items():
        get_db(game_data.identifier, companies).document(company_key).set(company.to_dict())
    for property_listings_key in game_data.property_listings:
        db_property_listings_ref.document(property_listings_key) \
            .set(game_data.property_listings[property_listings_key].to_dict())
    for market_listings_key in game_data.market_listings:
        db_market_listings_ref.document(market_listings_key) \
            .set(game_data.market_listings[market_listings_key].to_dict())
    for prop_key in game_data.properties:
        db_properties_ref.document(prop_key).set(game_data.properties[prop_key].to_dict())
    for product_key in game_data.products:
        get_db(game_data.identifier, products).document(product_key).set(game_data.products[product_key].to_dict())
    for buff_key in game_data.buffs:
        db_buffs_ref.document(buff_key).set(game_data.buffs[buff_key].to_dict())
    for currency_key in game_data.currencies:
        get_db(game_data.identifier, currencies).document(currency_key).set(game_data.currencies[currency_key].to_dict())
    # todo save records to local
    for user_profile_key, user_profile in game_data.user_profiles.items():
        get_db(game_data.identifier, user_profiles).document(user_profile_key).set(user_profile.to_dict())
    for company_key, stock_dict in game_data.company_stock_listings.items():
        col_ref = get_db(game_data.identifier, companies).document(company_key).collection(stock_listings)
        for listing_key, listing in stock_dict.items():
            col_ref.document(listing_key).set(listing.to_dict())


# market


def update_listing(game_data: GameData, listing_id: str):
    if listing_id in game_data.market_listings:
        listing = game_data.market_listings[listing_id]
        get_db(game_data.identifier, market_listings).document(listing_id).set(listing.to_dict())
    else:
        get_db(game_data.identifier).document(listing_id).delete()


def update_storage(game_data: GameData, storage: dict, products: dict):
    get_db(game_data.identifier, storages).set({k: storage[k] for k in products}, merge=True)
    get_db(game_data.identifier, storages).set({k: storage[k] for k in products}, merge=True)
