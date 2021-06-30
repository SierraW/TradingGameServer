class StockWallet(object):
    def __init__(self):
        self.company_stock_dict = dict()

    @staticmethod
    def from_dict(source):
        sw = StockWallet()
        sw.company_stock_dict = source['company_stock_dict']

    def to_dict(self):
        return {
            'company_stock_dict': self.company_stock_dict
        }
