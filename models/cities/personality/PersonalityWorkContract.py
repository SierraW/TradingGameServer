from models.TGTime import TGTime


class PersonalityWorkContract(object):
    def __init__(self, start_t: TGTime, end_t: TGTime, worker_id: str,
                 receiver_company_id: str,
                 receiver_property_id: str,
                 work_days: list[int],
                 one_time_payment: int,
                 salary_monthly: int,
                 provider_company_id: str = None,
                 provider_property_id: str = None,):
        self.start_t = start_t
        self.end_t = end_t
        self.worker_id = worker_id
        self.provider_company_id = provider_company_id
        self.provider_property_id = provider_property_id
        self.receiver_company_id = receiver_company_id
        self.receiver_property_id = receiver_property_id
        self.work_days = work_days
        self.one_time_payment = one_time_payment
        self.salary_monthly = salary_monthly
