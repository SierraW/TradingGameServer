from controllers.population_v2_controller import population_init_human
from controllers.financial_controller import register_financial_entity
from controllers.population_v2_controller import population_init_human
from controllers.property_controller import property_generate_property
from models.GameData import GameData
from models.cities.City import City
from models.cities.Market import Market


def city_init(game_data: GameData, data: dict):
    for key, source in data.items():
        city_original_dict = source
        market_settings = city_original_dict['market']
        market_fe_settings = market_settings['financial_id']
        market_fe_id = register_financial_entity(game_data=game_data, name=market_fe_settings['name'],
                                                 entity_type=4,
                                                 currency_dict=market_fe_settings['initial_fund_map'])
        market_property_id = property_generate_property(game_data=game_data, city_id=key, serial_name="1",
                                                        name=market_settings['property_name'])
        market = Market(city_id=key, financial_id=market_fe_id, property_id=market_property_id,
                        name=market_settings['name'], currency_id=city_original_dict['currency_id'],
                        handling_fee_rate=market_settings['handling_fee_rate'])
        city_original_dict['market'] = market.to_dict()

        financial_entity_settings = city_original_dict['financial_id']
        financial_entity_id = register_financial_entity(game_data=game_data, name=financial_entity_settings['name'],
                                                        entity_type=2,
                                                        currency_dict=financial_entity_settings['initial_fund_map'])
        city_original_dict['financial_id'] = financial_entity_id

        property_settings = city_original_dict['property']
        property_count = 0
        for property_name_count in property_settings['property_name_pool']:
            count = property_name_count[1]
            name = property_name_count[0]
            while count > 0:
                prop_id = property_generate_property(game_data=game_data, city_id=key, serial_name=f'{count}',
                                                     name=name)
                property_count += 1
                count -= 1
        city_original_dict['property_count'] = property_count

        city = City.from_dict(city_original_dict)
        game_data.cities[key] = city
        city.population_count = population_init_human(game_data=game_data, city_id=key, city=city)


def city_get_city(game_data: GameData, city_id: str) -> City:
    city = game_data.cities[city_id]
    city.city_id = city_id
    return city
