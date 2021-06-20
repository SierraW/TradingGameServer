class Product(object):
    def __init__(self, name, category):
        self.name = name
        self.category = category

    @staticmethod
    def from_dict(source):
        product = Product(source['name'], source['category'])
        return product

    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category
        }

    def __repr__(self):
        return f'Product(name={self.name}, category={self.category})'
