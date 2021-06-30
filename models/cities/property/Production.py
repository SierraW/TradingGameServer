from models.cities.property.Product import Product


class Production(object):
    def __init__(self, name: str, products: dict, level: int, size_multiplier: list[float], duration: int, consumes: dict = None):
        self.name = name
        self.consumes = consumes
        self.products = products
        self.level = level
        self.size_multiplier = size_multiplier
        self.duration = duration
        self.num_of_days_remaining = None
        self.buffs = dict()

    @staticmethod
    def from_dict(source):
        production = Production(name=source['name'], products=source['products'], level=source['level'],
                                size_multiplier=source['size_multiplier'], duration=source['duration'])
        if 'consumes' in source:
            production.consumes = source['consumes']
        if 'num_of_days_remaining' in source:
            production.num_of_days_remaining = source['num_of_days_remaining']
        if 'buffs' in source:
            production.buffs = source['buffs']
        return production

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'consumes': self.consumes,
            'product': self.products,
            'size_multiplier': self.size_multiplier,
            'duration': self.duration,
            'num_of_days_remaining': self.num_of_days_remaining,
            'buffs': self.buffs
        }

    def __repr__(self):
        return f'Production(name={self.name}, consumes={self.consumes}, product={self.products}, \
        duration={self.duration})'

    def get_consumes(self, level: int):
        if self.consumes is None:
            return None
        multiplied_consumes = {}
        for key, value in self.consumes:
            multiplied_consumes[key] = value * self.size_multiplier[level]
        return multiplied_consumes

    def start_production(self):
        self.num_of_days_remaining = self.duration
        self.buffs = dict()

    def get_multiplier(self, level: int) -> float:
        return self.size_multiplier[level]
