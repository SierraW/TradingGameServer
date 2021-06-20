class Currency(object):
    def __init__(self, name, prefix, symbol):
        self.name = name
        self.prefix = prefix
        self.symbol = symbol

    @staticmethod
    def from_dict(source):
        return Currency(source['name'], source['prefix'], source['symbol'])

    def to_dict(self):
        return {
            'name': self.name,
            'prefix': self.prefix,
            'symbol': self.symbol
        }

    def __repr__(self):
        return f'City(name={self.name}, prefix={self.prefix}, symbol={self.symbol})'
