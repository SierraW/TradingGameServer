from models.Human import Human


class Population(object):
    def __init__(self, humans=None):
        if humans is None:
            humans = []
        self.humans = []
        self.salaries = [0 * 4]

    @staticmethod
    def from_dict(source):
        population = Population()
        if 'humans' in source:
            population.humans = list(map(lambda human_dict: Human.from_dict(human_dict), source['humans']))
        if 'salaries' in source:
            population.salaries = source['salaries']
        return population

    def to_dict(self):
        return {
            'humans': list(map(lambda human: human.to_dict(), self.humans)),
            'salaries': self.salaries
        }

    def __repr__(self):
        return f'Population=(humans={self.humans})'

    def size(self, employed: bool = None) -> int:
        if employed is None:
            return len(self.humans)
        count = 0
        for human in self.humans:
            if employed:
                if human.property_id is not None:
                    count += 1
            else:
                if human.property_id is None:
                    count += 1
        return count
