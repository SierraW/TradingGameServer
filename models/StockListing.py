class StockListing(object):
    def __init__(self, seller_fe_id: str, amount: int, currency_id: str, price: int):
        self.seller_fe_id = seller_fe_id
        self.amount = amount
        self.currency_id = currency_id
        self.price = price
