

class Company(object):
    def __init__(self, financial_id, city_id, total_stock, auto_managed: bool, t_plus_created: int):
        self.financial_id = financial_id
        self.city_id = city_id
        self.total_stock = total_stock
        self.bankrupt_countdown = None
        self.budget_cap = 0
        self.auto_managed = auto_managed
        self.t_plus_created = t_plus_created

    @staticmethod
    def from_dict(source):
        company = Company(source['financial_id'], source['city_id'], source['total_stock'], source['auto_managed'],
                          source['t_plus_created'])
        if 'bankrupt_countdown' in source:
            company.bankrupt_countdown = source['bankrupt_countdown']
        return company

    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'city_id': self.city_id,
            'bankrupt_countdown': self.bankrupt_countdown,
            'total_stock': self.total_stock,
            'auto_managed': self.auto_managed,
            't_plus_created': self.t_plus_created
        }

    def __repr__(self):
        return f'Company(financial_id={self.financial_id})'
