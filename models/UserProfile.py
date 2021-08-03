class UserProfile(object):
    def __init__(self, financial_id: str):
        self.financial_id = financial_id

    @staticmethod
    def from_dict(source):
        return UserProfile(financial_id=source['financial_id'])

    def to_dict(self):
        return {
            'financial_id': self.financial_id
        }
