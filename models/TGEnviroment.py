from models.TGTime import TGTime


class TGEnvironment(object):
    def __init__(self):
        self.time = TGTime()
        self.identifier_factory = 0
        self.human_needs = []

    @staticmethod
    def from_dict(source):
        env = TGEnvironment()
        env.time = TGTime.from_dict(source['time'])
        env.identifier_factory = source['identifier_factory']
        env.human_needs = source['human_needs']

    def to_dict(self):
        return {
            'time': self.time,
            'identifier_factory': self.identifier_factory,
            'human_needs': self.human_needs
        }