

class Company(object):
    def __init__(self, financial_id, city_id, total_stock):
        self.financial_id = financial_id
        self.city_id = city_id
        self.total_stock = total_stock
        self.bankrupt_countdown = None
        self.budget_cap = 0

    @staticmethod
    def from_dict(source):
        company = Company(source['financial_id'], source['city_id'], source['total_stock'])
        if 'bankrupt_countdown' in source:
            company.bankrupt_countdown = source['bankrupt_countdown']
        return company

    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'city_id': self.city_id,
            'bankrupt_countdown': self.bankrupt_countdown,
            'total_stock': self.total_stock
        }

    def __repr__(self):
        return f'Company(financial_id={self.financial_id})'
