from models.cities.property.Product import Product


class Production(object):
    def __init__(self, name: str, products: dict, level: int, product_multiplier: list[float], duration: int,
                 consumes: dict = None,  consume_multiplier: list[float] = None):
        self.name = name
        self.consumes = consumes
        self.consume_multiplier = consume_multiplier
        self.products = products
        self.product_multiplier = product_multiplier
        self.level = level
        self.duration = duration
        self.num_of_days_remaining = None
        self.buffs = dict()

    @staticmethod
    def from_dict(source):
        production = Production(name=source['name'], products=source['products'], level=source['level'],
                                product_multiplier=source['product_multiplier'], duration=source['duration'])
        if 'consumes' in source:
            production.consumes = source['consumes']
        if 'consume_multiplier' in source:
            production.consume_multiplier = source['consume_multiplier']
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
            'consume_multiplier': self.consume_multiplier,
            'product': self.products,
            'product_multiplier': self.product_multiplier,
            'duration': self.duration,
            'num_of_days_remaining': self.num_of_days_remaining,
            'buffs': self.buffs
        }

    def __repr__(self):
        return f'Production(name={self.name}, consumes={self.consumes}, product={self.products}, \
        duration={self.duration})'

    def get_consumes(self, level: int) -> dict:
        multiplied_consumes = dict()
        if self.consumes is None:
            return multiplied_consumes
        for key, value in self.consumes.items():
            multiplied_consumes[key] = value * self.consume_multiplier[level]
        return multiplied_consumes

    def start_production(self):
        self.num_of_days_remaining = self.duration
        self.buffs = dict()

    def get_multiplier(self, level: int) -> float:
        return self.product_multiplier[level]
