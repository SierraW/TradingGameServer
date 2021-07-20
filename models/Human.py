from .Wallet import Wallet


class Human(object):
    def __init__(self, level: int):
        self.level = level
        self.buffs = {
            'wohaole': 0.0,
            'woele': 0.0,
            'buff_human_satisfaction': 0.0
        }
        self.property_id = None
        self.contract_remaining_days = None

    @staticmethod
    def from_dict(source):
        human = Human(level=source['level'])
        if 'buffs' in source:
            human.buffs = source['buffs']
        if 'property_id' in source:
            human.property_id = source['property_id']
        if 'contract_remaining_days' in source:
            human.chance_of_upgrade = source['contract_remaining_days']
        return human

    def to_dict(self):
        return {
            'level': self.level,
            'buffs': self.buffs,
            'property_id': self.property_id,
            'contract_remaining_days': self.contract_remaining_days
        }

    def __repr__(self):
        return f'Human(level={self.level})'
