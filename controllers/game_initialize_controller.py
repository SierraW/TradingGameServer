import json

from controllers.city_controller import city_init
from models.GameData import GameData
from models.cities.business.Management import Management
from models.cities.company.CompanyScope import CompanyScope
from models.cities.company.CompanyType import CompanyType
from models.cities.personality.PersonalityExperience import PersonalityExperience
from models.cities.property.Product import Product
from models.cities.business.Production import Production
from models.cities.property.Structure import Structure
from models.geometry.Currency import Currency


def init_from_local_essential(game_data: GameData) -> GameData:
    with open('../game_presets/currency.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.currencies[key] = Currency.from_dict(source=source)
    with open('../game_presets/company_scope.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.company_scopes[key] = CompanyScope.from_dict(source=source)
    with open('../game_presets/company_type.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.company_types[key] = CompanyType.from_dict(source=source)
    with open('../game_presets/experience.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.experiences[key] = PersonalityExperience.from_dict(source=source)
    with open('../game_presets/product.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.products[key] = Product.from_dict(source=source)
    with open('../game_presets/production.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.productions[key] = Production.from_dict(source=source)
    with open('../game_presets/management.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.management[key] = Management.from_dict(source=source)
    with open('../game_presets/structure.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.structures[key] = Structure.from_dict(source=source)
    with open('../game_presets/extras.json', 'r') as f:
        data = json.load(f)
        for key, source in data.items():
            game_data.structures[key] = source
    with open('../game_presets/city.json', 'r') as f:
        data = json.load(f)
        city_init(game_data=game_data, data=data)
    return game_data
