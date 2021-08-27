class Family(object):
    def __init__(self, family_last_name: str, family_member_id_list: list[str], financial_entity_id: str):
        self.family_last_name = family_last_name
        self.family_member_id_list = family_member_id_list
        self.financial_entity_id = financial_entity_id
