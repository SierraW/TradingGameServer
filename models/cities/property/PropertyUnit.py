from models.cities.business.Production import Production


class PropertyUnit(object):
    def __init__(self, owner_financial_entity_id: str, size: str, storage_id: str,
                 production_template_id: str, production: Production):
        self.owner_financial_entity_id = owner_financial_entity_id
        self.size = size
        self.storage_id = storage_id

        self.production_template_id = production_template_id
        self.production = production
