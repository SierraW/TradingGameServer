from models.cities.Market import Market
from models.cities.personality.Population import Population
from models.cities.property.Production import Production
from models.cities.property.Structure import Structure


class City(object):
    def __init__(self, country_id: str, name: str, financial_id: str, currency_id: str, market: Market,
                 population: dict, land_tax_per_year: int):
        self.country_id = country_id
        self.name = name
        self.financial_id = financial_id
        self.currency_id = currency_id
        self.structures = []
        self.population_count = 0
        self.population = population
        self.market = market
        self.property_count = 0
        self.land_tax_per_year = land_tax_per_year

    @staticmethod
    def from_dict(source):
        city = City(source['country_id'], source['name'], source['financial_id'], currency_id=source['currency_id'],
                    land_tax_per_year=source['land_tax_per_year'], population=source['population'],
                    market=Market.from_dict(source['market']))
        if 'structures' in source:
            city.structures = source['structures']
        if 'property_counter' in source:
            city.property_counter = source['property_counter']
        return city

    def to_dict(self):
        return {
            'country_id': self.country_id,
            'name': self.name,
            'financial_id': self.financial_id,
            'currency_id': self.currency_id,
            'structures': list(map(lambda structure: structure.to_dict(), self.structures)),
            'population': self.population,
            'market': self.market.to_dict(),
            'property_counter': self.property_count,
            'land_tax_per_year': self.land_tax_per_year
        }

    def __repr__(self):
        return self.to_dict().__repr__()
