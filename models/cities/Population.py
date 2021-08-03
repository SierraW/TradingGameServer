from models.Human import Human
from models.cities.HumanOffer import HumanOffer


class Population(object):
    def __init__(self, salaries: list[int], fe_accounts: list[str], storage_id: str, humans=None):
        if humans is None:
            humans = []
        self.humans = humans
        self.salaries = salaries
        self.fe_accounts = fe_accounts
        self.storage_id = storage_id
        self.offers = []

    @staticmethod
    def from_dict(source):
        population = Population(salaries=source['salaries'], fe_accounts=source['fe_accounts'],
                                storage_id=source['storage_id'])
        if 'humans' in source:
            population.humans = list(map(lambda human_dict: Human.from_dict(human_dict), source['humans']))
        if 'offers' in source:
            population.offers = list(map(lambda offer: HumanOffer.from_dict(offer), source['offers']))
        return population

    def to_dict(self):
        return {
            'humans': list(map(lambda human: human.to_dict(), self.humans)),
            'salaries': self.salaries,
            'fe_accounts': self.fe_accounts,
            'offers': list(map(lambda offer: offer.to_dict(), self.offers)),
            'storage_id': self.storage_id
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
