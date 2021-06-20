from models.cities.property.Property import Property
from models.cities.Population import Population
from models.cities.property.Production import Production
from models.cities.Market import Market


class City(object):
    def __init__(self, name):
        self.name = name
        self.productions = []
        self.population = Population()
        self.market = None

    @staticmethod
    def from_dict(source):
        city = City(source['name'])
        if 'productions' in source:
            city.productions = list(map(lambda production_dict: Production.from_dict(production_dict), source['productions']))
        if 'population' in source:
            city.population = Population.from_dict(source['population'])
        if 'market' in source:
            city.market = Market.from_dict(source['market'])
        return city

    def to_dict(self):
        return {
            'name': self.name,
            'productions': list(map(lambda production: production.to_dict(), self.productions)),
            'population': self.population.to_dict(),
            'market': self.market.to_dict()
        }

    def __repr__(self):
        return f'City(name={self.name})'
