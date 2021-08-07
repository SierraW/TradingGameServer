from models.cities.personality.Population import Population
from models.cities.property.Production import Production


class City(object):
    def __init__(self, country_id: str, name: str, financial_id: str, currency_id: str,
                 population: Population, land_tax_rate: float):
        self.country_id = country_id
        self.city_id = None
        self.name = name
        self.financial_id = financial_id
        self.currency_id = currency_id
        self.productions = []
        self.population = population
        self.market_id = None
        self.property_counter = 0
        self.land_tax_rate = land_tax_rate

    @staticmethod
    def from_dict(source):
        city = City(source['country_id'], source['name'], source['financial_id'], currency_id=source['currency_id'],
                    land_tax_rate=source['land_tax_rate'], population=Population.from_dict(source['population']))
        if 'productions' in source:
            city.productions = list(map(lambda production_dict: Production.from_dict(production_dict),
                                        source['productions']))
        if 'market_id' in source:
            city.market_id = source['market_id']
        if 'property_counter' in source:
            city.property_counter = source['property_counter']
        return city

    def to_dict(self):
        return {
            'country_id': self.country_id,
            'name': self.name,
            'financial_id': self.financial_id,
            'currency_id': self.currency_id,
            'productions': list(map(lambda production: production.to_dict(), self.productions)),
            'population': self.population.to_dict(),
            'market_id': self.market_id,
            'property_counter': self.property_counter,
            'land_tax_rate': self.land_tax_rate
        }

    def __repr__(self):
        return self.to_dict().__repr__()
