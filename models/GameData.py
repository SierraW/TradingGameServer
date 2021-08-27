import json

from models.TGEnviroment import TGEnvironment


class GameData(object):
    def __init__(self):
        self.identifier = 0
        self.environment = TGEnvironment()
        self.financial_entities = dict()
        self.companies = dict()
        self.storages = dict()
        self.countries = dict()
        self.cities = dict()
        self.markets = dict()
        self.property_listings = dict()
        self.market_listings = dict()
        self.properties = dict()
        self.buffs = dict()
        self.currencies = dict()
        self.market_reports = dict()
        self.user_profiles = dict()
        self.company_stock_listings = dict()

        self.humans = dict()
        self.career_fair = dict()
        self.work_contracts = dict()
        self.families = dict()
        self.company_scopes = dict()
        self.company_types = dict()
        self.experiences = dict()
        self.products = dict()
        self.productions = dict()
        self.structures = dict()
        self.extras = dict()

    def generate_identifier(self) -> str:
        self.environment.identifier_factory += 1
        return str(self.environment.identifier_factory)
