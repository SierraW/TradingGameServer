class TGTime(object):
    def __init__(self, year: int = 0, season: int = 0, day: int = 0, pause=False):
        self.year = year
        self.season = season
        self.day = day
        self.pause = pause

    @staticmethod
    def from_dict(source):
        return TGTime(source['year'], source['season'], source['day'], source['pause'])

    @staticmethod
    def get_t_plus_period_for_year(year: int) -> (int, int):
        start_t_plus = year * 30 * 4
        end_t_plus = start_t_plus + (30 * 4) - 1
        return start_t_plus, end_t_plus

    def to_dict(self):
        return {
            'year': self.year,
            'season': self.season,
            'day': self.day,
            'pause': self.pause
        }

    def elapsed(self):
        if self.day == 29:
            self.day = 0
            if self.season == 3:
                self.season = 0
                self.year += 1
            else:
                self.season += 1
        else:
            self.day += 1

    def print_season(self) -> str:
        season_str = ['Spring', 'Summer', 'Autumn', 'Winter']
        return season_str[self.season]

    def __repr__(self):
        return f'{self.year + 1}Y {self.print_season()} {self.day + 1}Day'

    def get_t_plus_from_now(self, year: int = 0, season: int = 0, day: int = 0) -> int:
        return ((self.year + year) * 4 + (self.season + season)) * 30 + self.day + day

    def is_new_years_day(self) -> bool:
        return self.season == 0 and self.day == 0

