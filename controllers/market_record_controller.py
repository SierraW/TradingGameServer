from data import GameData
from models.cities.MarketReceipt import MarketPurchaseReceipt
from models.report.MarketReport import MarketReport, ProductReport


def init_records(game_data: GameData):
    for market_id in game_data.markets:
        if market_id not in game_data.market_reports:
            game_data.market_reports[market_id] = []
        game_data.market_reports[market_id].insert(0, MarketReport())
        if len(game_data.market_reports[market_id]) > 360:
            del game_data.market_reports[market_id][-1]


def get_reports_for_market(game_data: GameData, market_id: str, pos: int,
                           num_of_reports: int = 0) -> list[MarketReport]:
    marketReportList = game_data.market_reports[market_id]
    start_pos = len(marketReportList) - pos
    if start_pos < 0:
        start_pos = 0
    end_pos = start_pos + num_of_reports
    if end_pos > len(marketReportList):
        end_pos = len(marketReportList)
    return marketReportList[start_pos:end_pos]


def get_product_report_from_market_reports(market_reports: list[MarketReport], product_id: str) -> ProductReport:
    product_report = ProductReport()
    for market_report in market_reports:
        report = market_report.get_report(product_id=product_id)
        product_report.record(sold_amount=report.sold_amount, currency_id=report.currency_id,
                              total_price=report.total_price)
    return product_report


def submit_receipt(game_data: GameData, receipt: MarketPurchaseReceipt):
    if receipt.market_id not in game_data.market_reports:
        print(f'market_reports for {receipt.market_id} not initialized')
        return
    game_data.market_reports[receipt.market_id][0].submit_report(receipt=receipt)


def get_previous_average_price(game_data: GameData, market_id: str, product_id: str, currency_id: str = None) -> int:
    if market_id in game_data.market_reports:
        report = game_data.market_reports[market_id][0]
        product_report = report.get_report(product_id=product_id)
        if product_report is not None and (currency_id is None or product_report.currency_id is currency_id):
            if product_report.total_price > 0 and product_report.sold_amount > 0:
                return int(product_report.total_price / product_report.sold_amount)
