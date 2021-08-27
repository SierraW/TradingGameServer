import debug_toolkit


class TGTime(object):
    def __init__(self, year: int = 1979, month: int = 0, day: int = 0, weekday: int = 0, pause=False):
        if year < 1979:
            debug_toolkit.warning_print('TGTime init', 'Year should not be less than 1979', [f'{year}'])
            return
        self.year = year
        self.month = month
        self.day = day
        self.weekday = weekday
        self.pause = pause

    @staticmethod
    def from_dict(source):
        return TGTime(source['year'], source['month'], source['day'], source['weekday'], source['pause'])

    @staticmethod
    def get_t_plus_period_for_year(year: int) -> (int, int):
        start_t_plus = year * 30 * 4
        end_t_plus = start_t_plus + (30 * 4) - 1
        return start_t_plus, end_t_plus

    @staticmethod
    def from_date(year: int, month: int, day: int):
        if year < 1979:
            year = 1979
        if month < 1:
            month = 1
        if day < 1:
            day = 1
        return TGTime().offset(year - 1979, month - 1, day - 1)

    @staticmethod
    def from_t_plus(t_plus: int, t=None):
        year = 1979 if t is None else t.year
        month = 0 if t is None else t.month
        day = 0 if t is None else t.day
        week = (t_plus + (0 if t is None else t.weekday)) % 7
        is_leap_year = TGTime.is_leap_year(year)
        while t_plus > (365 if is_leap_year else 365):
            t_plus -= (366 if is_leap_year else 365)
            year += 1
            is_leap_year = TGTime.is_leap_year(year)
        day += t_plus
        num_of_days = TGTime.get_number_of_days_in_month(year=year, month=month)
        while day >= num_of_days:
            day -= num_of_days
            if month == 11:
                year += 1
                month = 0
            else:
                month += 1
            num_of_days = TGTime.get_number_of_days_in_month(year=year, month=month)
        return TGTime(year=year, month=month, day=day, weekday=week)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    @staticmethod
    def get_number_of_days_in_month(year: int, month: int) -> int:
        month_days_list = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 1:
            if TGTime.is_leap_year(year):
                return 29
            else:
                return 28
        else:
            return month_days_list[month]

    def copy(self):
        return TGTime(year=self.year, month=self.month, day=self.day, weekday=self.weekday, pause=self.pause)

    def offset(self, year: int = 0, month: int = 0, day: int = 0):
        delta_t_plus = day
        temp_year = self.year
        while year > 0:
            delta_t_plus += (366 if TGTime.is_leap_year(year=temp_year) else 365)
            temp_year += 1
            year -= 1
        temp_month = self.month
        while month > 0:
            delta_t_plus += TGTime.get_number_of_days_in_month(year=temp_year, month=temp_month)
            if temp_month == 11:
                temp_month = 0
                temp_year += 1
            else:
                temp_month += 1
            month -= 1
        return TGTime.from_t_plus(t_plus=delta_t_plus, t=self)

    def get_total_work_days(self, end_t_plus: int, work_days: list[int]) -> int:  # TODO improve this
        week_list = [0] * 7
        week = self.weekday
        while end_t_plus > 0:
            week_list[week] += 1
            if week == 6:
                week = 0
            else:
                week += 1
            end_t_plus -= 1
        count = 0
        for day_in_week in work_days:
            count += week_list[day_in_week]
        return count

    def to_dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'weekday': self.weekday,
            'pause': self.pause,
        }

    def elapse(self):
        if self.day >= TGTime.get_number_of_days_in_month(year=self.year, month=self.month) - 1:
            self.day = 0
            if self.month == 11:
                self.month = 0
                self.year += 1
            else:
                self.month += 1
        else:
            self.day += 1
        if self.weekday == 6:
            self.weekday = 0
        else:
            self.weekday += 1

    def print_season(self) -> str:
        month_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return month_str[self.month]

    def print_weekday(self) -> str:
        week_str = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return week_str[self.weekday]

    def __repr__(self):
        return f'{self.year}-{self.print_season()}-{self.day + 1} {self.print_weekday()}'

    def get_t_plus_from_now(self, year: int = 0, month: int = 0, day: int = 0) -> int:
        new_year = year + self.year
        new_month = month + self.month
        while new_month > 12:
            new_year += 1
            new_month -= 12

        return ((self.year + year) * 4 + (self.month + month)) * 30 + self.day + day

    def is_new_years_day(self) -> bool:
        return self.month == 0 and self.day == 0
