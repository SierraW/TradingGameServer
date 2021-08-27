class PersonalityExperience(object):
    def __init__(self, name: str, description: str, formation_time: int):
        self.name = name
        self.description = description
        self.formation_time = formation_time

    @staticmethod
    def from_dict(source):
        return PersonalityExperience(name=source['name'],
                                     description=source['description'],
                                     formation_time=source['formation_time'])

    def __repr__(self):
        return f'Experience: {self.name} {self.formation_time}'
