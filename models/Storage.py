class Storage(object):
    def __init__(self, products=None):
        if products is None:
            products = dict()
        self.products = products

    @staticmethod
    def from_dict(source):
        storage = Storage(source)
        return storage

    def to_dict(self):
        return {
            'products': self.products
        }

    def __repr__(self):
        return f'Storage(products={self.products})'

    def remove(self, product, count) -> bool:
        if product in self.products:
            if self.products[product] >= count:
                self.products[product] -= count
                return True
        return False

    def add(self, product, count):
        if product not in self.products:
            self.products[product] = count
        else:
            self.products[product] += count
