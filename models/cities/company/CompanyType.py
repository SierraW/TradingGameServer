class CompanyType(object):
    def __init__(self,
                 name: str,
                 company_scope_id: str,
                 designated_structures: list[str],
                 stock_market_visibility: int,
                 stock_market_access_type: int):
        self.name = name
        self.company_scope_id = company_scope_id
        self.designated_structures = designated_structures
        self.stock_market_visibility = stock_market_visibility
        self.stock_market_access_type = stock_market_access_type

    @staticmethod
    def from_dict(source):
        return CompanyType(name=source['name'], company_scope_id=source['company_scope_id'],
                           designated_structures=source['designated_structures'],
                           stock_market_visibility=source['stock_market_visibility'],
                           stock_market_access_type=source['stock_market_access_type'])
