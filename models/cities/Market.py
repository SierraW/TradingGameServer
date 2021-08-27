class Market(object):
    def __init__(self, city_id, financial_id, property_id, name, currency_id: str, handling_fee_rate):
        self.financial_id = financial_id
        self.property_id = property_id
        self.city_id = city_id
        self.name = name
        self.currency_id = currency_id
        self.handling_fee_rate = handling_fee_rate

    @staticmethod
    def from_dict(source):
        market = Market(financial_id=source['financial_id'],
                        property_id=source['property_id'], name=source['name'], currency_id=source['currency_id'],
                        handling_fee_rate=source['handling_fee_rate'], city_id=source['city_id'])
        return market

    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'city_id': self.city_id,
            'property_id': self.property_id,
            'name': self.name,
            'currency_id': self.currency_id,
            'handling_fee_rate': self.handling_fee_rate
        }
