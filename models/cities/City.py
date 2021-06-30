from models.cities.property.Property import Property
from models.cities.Population import Population
from models.cities.property.Production import Production
from models.cities.Market import Market


class City(object):
    def __init__(self, country_id: str, name: str, financial_id: str, currency_id: str):
        self.country_id = country_id
        self.city_id = None
        self.name = name
        self.financial_id = financial_id
        self.currency_id = currency_id
        self.productions = []
        self.population = Population()
        self.market_id = None
        self.property_counter = 0

    @staticmethod
    def from_dict(source):
        city = City(source['country_id'], source['name'], source['financial_id'], currency_id=source['currency_id'])
        if 'productions' in source:
            city.productions = list(map(lambda production_dict: Production.from_dict(production_dict), source['productions']))
        if 'population' in source:
            city.population = Population.from_dict(source['population'])
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
        }

    def __repr__(self):
        return f'City(name={self.name})'
