class Product(object):
    def __init__(self, name: str, category: int, items_per_stack: int = None):
        self.name = name
        self.category = category
        self.items_per_stack = items_per_stack

    @staticmethod
    def from_dict(source):
        return Product(name=source['name'], category=source['category'], items_per_stack=source['items_per_stack'])

    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'items_per_stack': self.items_per_stack
        }
