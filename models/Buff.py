class Buff(object):
    def __init__(self, name: str, effects: list[str], key_effects_data: list[float],
                 description: str):
        self.name = name
        self.effects = effects
        self.key_effect_data = key_effects_data
        self.description = description

    @staticmethod
    def from_dict(source):
        buff = Buff(source['name'], source['effects'], source['key_effect_data'], source['description'])
        return buff

    def to_dict(self):
        return {
            'name': self.name,
            'effects': self.effects,
            'key_effect_data': self.key_effect_data,
            'description': self.description
        }

    def get_effects_str(self) -> list[str]:
        detailed_effects = []
        count = 0
        for effect in self.effects:
            if count >= len(self.key_effect_data):
                detailed_effects.append(effect)
            else:
                detailed_effects.append(effect.replace('/$', str(self.key_effect_data[count])))
            count += 1
        return detailed_effects
