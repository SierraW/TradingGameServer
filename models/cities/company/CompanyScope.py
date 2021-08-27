class CompanyScope(object):
    def __init__(self, name: str, designated_structure: list):
        self.name = name
        self.designated_structure = designated_structure

    @staticmethod
    def from_dict(source):
        return CompanyScope(name=source['name'], designated_structure=source['designated_structure'])