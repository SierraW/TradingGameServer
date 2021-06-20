

class Company(object):
    def __init__(self, financial_id):
        self.financial_id = financial_id
        self.bankrupt_countdown = None

    @staticmethod
    def from_dict(source):
        company = Company(source['financial_id'])
        if 'bankrupt_countdown' in source:
            company.bankrupt_countdown = source['bankrupt_countdown']
        return company

    def to_dict(self):
        return {
            'financial_id': self.financial_id,
            'bankrupt_countdown': self.bankrupt_countdown
        }

    def __repr__(self):
        return f'Company(financial_id={self.financial_id})'
