class HumanOffer(object):
    def __init__(self, company_id: str, property_id: str, level: int, one_time_payment: int):
        self.company_id = company_id
        self.property_id = property_id
        self.level = level
        self.one_time_payment = one_time_payment

    @staticmethod
    def from_dict(source):
        return HumanOffer(company_id=source['company_id'], property_id=source['property_id'], level=source['level'],
                          one_time_payment=source['one_time_payment'])

    def to_dict(self):
        return {
            'company_id': self.company_id,
            'property_id': self.property_id,
            'level': self.level,
            'one_time_payment': self.one_time_payment
        }

    def __repr__(self):
        return self.to_dict().__repr__()
