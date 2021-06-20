from models.Human import Human


class Population(object):
    def __init__(self, humans=None):
        if humans is None:
            humans = []
        self.humans = []
        self.natural_growth_rate = 1.0


    @staticmethod
    def from_dict(source):
        population = Population()
        if 'humans' in source:
            population.humans = list(map(lambda human_dict: Human.from_dict(human_dict), source['humans']))
        return population

    def to_dict(self):
        return {
            'humans': list(map(lambda human: human.to_dict(), self.humans))
        }

    def __repr__(self):
        return f'Population=(humans={self.humans})'
