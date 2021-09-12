class CompanyType(object):
    def __init__(self,
                 name: str,
                 company_scope_id: str,
                 stock_market: dict):
        self.name = name
        self.company_scope_id = company_scope_id
        self.stock_market = stock_market

    @staticmethod
    def from_dict(source):
        return CompanyType(name=source['name'], company_scope_id=source['company_scope_id'],
                           stock_market=source['stock_market'])
