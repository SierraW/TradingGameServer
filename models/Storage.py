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

    def remove_as_much_as_possible(self, product_id: str, amount: int) -> int:
        if product_id in self.products:
            removed_amount = amount if self.products[product_id] >= amount else self.products[product_id]
            self.products[product_id] -= removed_amount
            return removed_amount
        else:
            return 0

    def remove(self, products: dict) -> bool:
        items_removed = dict()
        is_success = True
        for product, amount in products.items():
            if product in self.products and self.products[product] >= amount:
                self.products[product] -= amount
                items_removed[product] = amount
            else:
                is_success = False
                break
        if not is_success:
            self.combine(items_removed)
            return False
        return True

    def add(self, product, count):
        if product not in self.products:
            self.products[product] = count
        else:
            self.products[product] += count

    def combine(self, products_dict: dict):
        for product_id, amount in products_dict.items():
            self.add(product_id, amount)
