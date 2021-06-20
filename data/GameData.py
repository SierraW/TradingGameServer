from database import *
from models.TGEnviroment import TGEnvironment
from models.TGTime import TGTime


class GameData(object):
    def __init__(self):
        self.identifier = 0
        self.environment = TGEnvironment()
        self.financial_entities = {}  # watch me
        self.storages = {}  # watch me
        self.countries = []
        self.cities = {}
        self.property_listings = {}
        self.market_listings = {}
        self.properties = {}
        self.products = {}
        self.buffs = {}
        self.currencies = {}

    def generate_identifier(self) -> str:
        self.environment.identifier_factory += 1
        return str(self.environment.identifier_factory)

    def register_market_listing(self, market_listing) -> str:
        ml_id = self.generate_identifier()
        self.market_listings[ml_id] = market_listing  # todo: replaced with auto update
        db_market_listings_ref.document(ml_id).set(market_listing.to_dict())
        return ml_id

    @staticmethod
    def from_backup(filename):
        game_data = GameData()

        pass

    @staticmethod
    def from_cloud(game_id: str):
        game_data = GameData()
        game_data.identifier = game_id
        time_doc = get_db(game_id, environment).document('time').get()
        if time_doc.exists:
            game_data.environment.time = TGTime.from_dict(time_doc.to_dict())

        return game_data

    def backup(self):
        pass

    def to_cloud(self):
        db_time_ref.set(self.environment.time.to_dict())
        db_identifier_factory_ref.set({'0': self.environment.identifier_factory})
        for entity_key in self.financial_entities:
            db_financial_entities_ref.document(entity_key).set(self.financial_entities[entity_key].to_dict())
        for storage_key in self.storages:
            db_storages_ref.document(storage_key).set(self.storages[storage_key].to_dict())
        for country in self.countries:
            db_countries_ref.document(country.name).set(country.to_dict())
        for city_key in self.cities:
            db_cities_ref.document(city_key).set(self.cities[city_key].to_dict())
        for property_listings_key in self.property_listings:
            db_property_listings_ref.document(property_listings_key)\
                .set(self.property_listings[property_listings_key].to_dict())
        for market_listings_key in self.market_listings:
            db_market_listings_ref.document(market_listings_key)\
                .set(self.market_listings[market_listings_key].to_dict())
        for prop_key in self.properties:
            db_properties_ref.document(prop_key).set(self.properties[prop_key].to_dict())
        for product_key in self.products:
            get_db(self.identifier, products).document(product_key).set(self.products[product_key].to_dict())
        for buff_key in self.buffs:
            db_buffs_ref.document(buff_key).set(self.buffs[buff_key].to_dict())
        for currency_key in self.currencies:
            get_db(self.identifier, currencies).document(currency_key).set(self.currencies[currency_key].to_dict())
        print(f'{self.identifier} has been successfully uploaded')

