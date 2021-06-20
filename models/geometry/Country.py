from .Currency import Currency
from models.cities.City import City


class Country(object):
    def __init__(self, name, currency_id, tax_rate):
        self.name = name
        self.currency_id = currency_id
        self.tax_rate = tax_rate
        self.cities = []

    @staticmethod
    def from_dict(source):
        country = Country(name=source['name'], currency_id=Currency.from_dict(source['currency_id']),
                          tax_rate=Currency.from_dict(source['tax_rate']))
        if 'cities' in source:
            country.cities = source['cities']
        return country

    def to_dict(self):
        return {
            'name': self.name,
            'currency_id': self.currency_id,
            'tax_rate': self.tax_rate,
            'cities': self.cities
        }

    def __repr__(self):
        return f'Country(name={self.name}, currency={self.currency_id}, tax_rate={self.tax_rate})'
