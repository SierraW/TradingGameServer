from models.GameData import GameData
from models.cities.property.Product import Product


def product_get_products_by_category(game_data: GameData, category: int) -> dict:
    return dict(filter(lambda pid_product: pid_product[1].category == category, game_data.products.items()))
