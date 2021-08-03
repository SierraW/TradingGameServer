

class Company(object):
    def __init__(self, financial_id: str, city_id: str, total_stock: int, company_type: int, auto_managed: bool,
                 t_plus_created: int, property_id: str = None, reminder: dict = None):
        self.financial_id = financial_id
        self.city_id = city_id
        self.total_stock = total_stock
        self.property_id = property_id
        self.company_type = company_type
        self.budget_cap = 0
        self.auto_managed = auto_managed
        self.t_plus_created = t_plus_created
        self.reminder = reminder if reminder is not None else dict()

    @staticmethod
    def from_dict(source):
        company = Company(financial_id=source['financial_id'], city_id=source['city_id'],
                          total_stock=source['total_stock'], company_type=source['company_type'],
                          auto_managed=source['auto_managed'], t_plus_created=source['t_plus_created'],
                          property_id=source['property_id'], reminder=source['reminder'])
        return company

    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'city_id': self.city_id,
            'company_type': self.company_type,
            'total_stock': self.total_stock,
            'auto_managed': self.auto_managed,
            't_plus_created': self.t_plus_created,
            'property_id': self.property_id,
            'reminder': self.reminder
        }

    def __repr__(self):
        return self.to_dict().__repr__()
