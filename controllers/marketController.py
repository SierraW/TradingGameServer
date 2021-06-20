from controllers.financialController import transfer
from data import GameData
from models.cities.City import City
from database import get_db, market_listings


def purchase_single(game_data: GameData, buyer_fe_id: str, listing_id: str, amount: int) -> bool:
    if listing_id in game_data.market_listings:
        listing = game_data.market_listings[listing_id]
        if listing.amount >= amount:
            if transfer(game_data=game_data, sender_fe_id=buyer_fe_id, receiver_fe_id=listing.seller_fe_id,
                        currency_id=listing.currency_id, amount=amount):
                listing.amount -= amount
                if listing.amount == 0:
                    del game_data.market_listings[listing_id]
                update_listing(game_data, listing_id)
                return True
    return False


def purchase(buyer_fe_id: str, products: dict, city: City) -> bool:
    # todo finish purchase
    pass


def update_listing(game_data: GameData, listing_id: str):
    if listing_id in game_data.market_listings:
        listing = game_data.market_listings[listing_id]
        get_db(game_data.identifier, market_listings).document(listing_id).set(listing.to_dict())
    else:
        get_db(game_data.identifier).document(listing_id).delete()
