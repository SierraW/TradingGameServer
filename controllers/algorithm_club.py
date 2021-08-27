import random

from models.cities.personality.Human import Human


def random_choice(choice: list):
    return random.choice(choice)

def random_range(range_list: list[int]) -> int:
    return random.randint(range_list[0], range_list[1])


def random_check(possibility: float) -> bool:
    if possibility > 1:
        return True
    return random.random() < possibility


def find_most_common_level(humans: list[Human]) -> int:
    elements_remaining = len(humans)
    level_list = [0] * 4
    most_common_level = -1
    for human in humans:
        level_list[human.level] += 1
        elements_remaining -= 1
        if most_common_level == -1:
            most_common_level = human.level
        else:
            frequency = level_list[human.level]
            history_frequency = level_list[most_common_level]
            if human.level != most_common_level:
                if frequency == history_frequency:
                    if human.level > most_common_level:
                        most_common_level = human.level
                elif frequency > history_frequency:
                    most_common_level = human.level
            if level_list[most_common_level] > elements_remaining:
                break
    return most_common_level


def find_desired_employee_amount(num_of_employee: int) -> int:
    return 9 if num_of_employee > 6 else 3
