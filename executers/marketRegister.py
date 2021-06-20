from data import GameData, get_game_data
from models.cities.MarketListing import MarketListing

# payload = {
#     'market_id': '123',
#     'seller_fe_id': '311',
#     'product': 'obj_product',
#     'amount': 123,
#     'price': 123
# }


def production_register(command):
    game_data = get_game_data(command.game_id)
    payload = command.payload
    ml = MarketListing(payload['market_id'], payload['seller_fe_id'], payload['product'],
                       payload['amount'], payload['price'])
    game_data.register_market_listing(ml)
