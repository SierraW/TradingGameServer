class CompanyScope(object):
    def __init__(self, name: str, designated_business: list):
        self.name = name
        self.designated_business = designated_business

    @staticmethod
    def from_dict(source):
        return CompanyScope(name=source['name'], designated_business=source['designated_business'])