class PersonalityOffer(object):
    def __init__(self, company_id: str, property_id: str, work_days: list[int], monthly_salary: int,
                 one_time_payment: int, expired_in: int, duration_months: int):
        self.company_id = company_id
        self.property_id = property_id
        self.monthly_salary = monthly_salary
        self.work_days = work_days
        self.one_time_payment = one_time_payment
        self.expired_in = expired_in
        self.duration_months = duration_months

    @staticmethod
    def from_dict(source):
        return PersonalityOffer(company_id=source['company_id'],
                                property_id=source['property_id'],
                                work_days=source['work_days'],
                                monthly_salary=source['monthly_salary'],
                                one_time_payment=source['one_time_payment'],
                                expired_in=source['expired_in'],
                                duration_months=source['duration_months'])

    def to_dict(self):
        return {
            'company_id': self.company_id,
            'property_id': self.property_id,
            'work_days': self.work_days,
            'monthly_salary': self.monthly_salary,
            'one_time_payment': self.one_time_payment,
            'expired_in': self.expired_in,
            'duration_months': self.duration_months
        }

    def __repr__(self):
        return self.to_dict().__repr__()
