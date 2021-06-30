from data import GameData
from models.cities.MarketReceipt import MarketPurchaseReceipt
from models.report.MarketReport import MarketReport


def init_records(game_data: GameData):
    for market_id in game_data.markets:
        if market_id not in game_data.market_reports:
            game_data.market_reports[market_id] = []
        game_data.market_reports[market_id].insert(0, MarketReport())
        if len(game_data.market_reports[market_id]) > 360:
            del game_data.market_reports[market_id][-1]


def submit_receipt(game_data: GameData, receipt: MarketPurchaseReceipt):
    if receipt.market_id not in game_data.market_reports:
        print(f'market_reports for {receipt.market_id} not initialized')
        return
    game_data.market_reports[receipt.market_id].submit_report(receipt=receipt)


def get_previous_average_price(game_data: GameData, market_id: str, product_id: str, currency_id: str) -> int:
    report = game_data.market_reports[market_id]
    if report is not None:
        product_report = report.get_report(product_id=product_id)
        if product_report is not None and product_report.currency_id is currency_id:
            if product_report.total_price > 0 and product_report.sold_amount > 0:
                return int(product_report.total_price / product_report.sold_amount)
