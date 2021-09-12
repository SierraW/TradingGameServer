from models.TGTime import TGTime


class Company(object):
    def __init__(self, financial_id: str, city_id: str, total_stock: int,
                 company_type: int, auto_managed: bool,
                 date_create: TGTime, registered_property_id: str = None,
                 businesses: list = None):
        self.financial_id = financial_id
        self.city_id = city_id
        self.total_stock = total_stock
        self.registered_property_id = registered_property_id
        self.company_type = company_type
        self.auto_managed = auto_managed
        self.date_create = date_create
        if businesses is None:
            self.businesses = []
        else:
            self.businesses = businesses

    @staticmethod
    def from_dict(source):
        company = Company(financial_id=source['financial_id'], city_id=source['city_id'],
                          total_stock=source['total_stock'], company_type=source['company_type'],
                          auto_managed=source['auto_managed'], date_create=source['date_create'],
                          registered_property_id=source['registered_property_id'])
        if 'businesses' in source:
            company.businesses = source['businesses']
        return company

    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'city_id': self.city_id,
            'company_type': self.company_type,
            'total_stock': self.total_stock,
            'auto_managed': self.auto_managed,
            'date_create': self.date_create,
            'registered_property_id': self.registered_property_id,
        }

    def __repr__(self):
        return self.to_dict().__repr__()
