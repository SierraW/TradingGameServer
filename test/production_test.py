from controllers import init_records
from controllers.game_init import init_game_with_defaults
from controllers.user_profile_controller import register_user_profile
from models.cities.property.Product import Product
from controllers.market_controller import *
from controllers.company_controller import *
from controllers.property_controller import *
from controllers.population_controller import *
from controllers.city_controller import *

game_data = GameData()
init_game_with_defaults(game_data=game_data)

gold_id = 'GOLD'
wheat = "小麦"
clothes = "布料"

heidal_city_id = "海德尔"
heidal_city = game_data.cities[heidal_city_id]
heidal_city_fe = game_data.financial_entities[heidal_city.financial_id]

heidal_city_market = game_data.markets[heidal_city.market_id]
heidal_city_market_fe = game_data.financial_entities[heidal_city_market.financial_id]

for _ in range(360):
    init_records(game_data=game_data)
    population_loop(game_data=game_data, city=heidal_city)
    cities_loop(game_data=game_data)
    companies_loop(game_data=game_data)
    properties_loop(game_data=game_data)
    game_data.environment.time.elapsed()

print(heidal_city_market)
