

class PropertyListing(object):
    def __init__(self, city_id: str, property_id: str, currency_id: str, price: int):
        self.city_id = city_id
        self.property_id = property_id
        self.currency_id = currency_id
        self.price = price

    @staticmethod
    def from_dict(source):
        return PropertyListing(city_id=source['city_id'], property_id=source['property_id'],
                               currency_id=source['currency_id'], price=source['price'])

    def to_dict(self):
        return {
            'city_id': self.city_id,
            'property_id': self.property_id,
            'currency_id': self.currency_id,
            'price': self.price
        }
