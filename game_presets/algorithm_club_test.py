from controllers.algorithm_club import *

true_count = 0
false_count = 0
for _ in range(100):
    chance = 1
    if random_check(possibility=chance):
        true_count += 1
    else:
        false_count += 1
