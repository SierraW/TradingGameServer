from models.cities.MarketReceipt import MarketPurchaseReceipt


class ProductReport(object):
    def __init__(self):
        self.sold_amount = 0
        self.currency_id = None
        self.total_price = 0

    def record(self, sold_amount: int, currency_id: str, total_price: int):
        if self.currency_id is None:
            self.sold_amount = sold_amount
            self.currency_id = currency_id
            self.total_price = total_price
        elif self.currency_id == currency_id:
            self.sold_amount += sold_amount
            self.total_price += total_price


class MarketReport(object):
    def __init__(self):
        self.product_report_dict = dict()

    def submit_report(self, receipt: MarketPurchaseReceipt):
        if receipt.product_id not in self.product_report_dict:
            self.product_report_dict[receipt.product_id] = ProductReport()
        self.product_report_dict[receipt.product_id].record(sold_amount=receipt.amount, total_price=receipt.total_price)

    def get_report(self, product_id) -> ProductReport:
        return self.product_report_dict[product_id]
