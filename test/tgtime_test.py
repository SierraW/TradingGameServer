from models.TGTime import TGTime

t_plus = 0

time1979 = TGTime.from_t_plus(t_plus=t_plus)

time1980 = TGTime.from_t_plus(365, time1979)
time1980_2 = time1979.offset(year=1)
time1980_3 = time1979.offset(month=12)

time1981 = TGTime.from_t_plus(366, time1980)
time1981_2 = time1979.offset(year=2)
time1981_3 = time1979.offset(month=24)

time2021 = TGTime.from_date(2021, 8, 19)
time2021_2 = TGTime.from_t_plus(15571, time1979)
time2021_3 = time1979.offset(year=42, month=7, day=18)

time_error = TGTime.from_date(1700, 0, 0)
