from models.cities.property.ProductInformation import ProductInformation


class BonusPackage(object):
    def __init__(self,
                 designo_multiplier: float,
                 software_solution_multiplier: float,
                 raw_material_multiplier: float,
                 employee_experience_multiplier: float,
                 designo_product_id: str = None,
                 designo_product_information: ProductInformation = None,
                 software_product_id: str = None,
                 software_product_product_information: ProductInformation = None):
        self.designo_product_id = designo_product_id
        self.designo_product_information = designo_product_information
        self.designo_multiplier = designo_multiplier
        self.software_product_id = software_product_id
        self.software_product_product_information = software_product_product_information
        self.software_solution_multiplier = software_solution_multiplier
        self.raw_material_multiplier = raw_material_multiplier
        self.employee_experience_multiplier = employee_experience_multiplier

    @staticmethod
    def from_dict(source):
        bonus_package = BonusPackage(designo_multiplier=source['designo_multiplier'],
                                     software_solution_multiplier=source['software_solution_multiplier'],
                                     raw_material_multiplier=source['raw_material_multiplier'],
                                     employee_experience_multiplier=source['employee_experience_multiplier'])
        if 'designo_product_id' in source:
            bonus_package.designo_product_id = source['designo_product_id']
        if 'designo_product_information' in source:
            bonus_package.designo_product_information = \
                ProductInformation.from_dict(source['designo_product_information'])
        if 'software_product_id' in source:
            bonus_package.software_product_id = source['software_product_id']
        if 'software_product_product_information' in source:
            bonus_package.software_product_product_information = \
                ProductInformation.from_dict(source['software_product_product_information'])
