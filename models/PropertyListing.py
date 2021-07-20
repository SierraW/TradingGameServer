

class PropertyListing(object):
    def __init__(self, city_id: str, property_id: str, currency_id: str, price: int, target_buyer_fe_id: str = None):
        self.city_id = city_id
        self.property_id = property_id
        self.currency_id = currency_id
        self.price = price
        self.target_buyer_fe_id = target_buyer_fe_id

    @staticmethod
    def from_dict(source):
        return PropertyListing(city_id=source['city_id'], property_id=source['property_id'],
                               currency_id=source['currency_id'], price=source['price'],
                               target_buyer_fe_id=source['target_buyer_fe_id'])

    def to_dict(self):
        return {
            'city_id': self.city_id,
            'property_id': self.property_id,
            'currency_id': self.currency_id,
            'price': self.price,
            'target_buyer_fe_id': self.target_buyer_fe_id
        }

    def __repr__(self):
        return self.to_dict().__repr__()
