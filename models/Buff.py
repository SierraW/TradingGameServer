class Buff(object):
    def __init__(self, name: str, effects: list[str], description: str, effective_days_remaining: int = None):
        self.name = name
        self.effects = effects
        self.description = description
        self.effective_days_remaining = None

    @staticmethod
    def from_dict(source):
        buff = Buff(source['name'], source['effects'], source['description'])
        if 'effective_days_remaining' in source:
            buff.effective_days_remaining = source['effective_days_remaining']
        return buff

    def to_dict(self):
        return {
            'name': self.name,
            'effects': self.effects,
            'description': self.description,
            'effective_days_remaining': self.effective_days_remaining
        }
