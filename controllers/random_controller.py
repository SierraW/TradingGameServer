from random import random


def check_random_result(chance: float) -> bool:
    return random() < chance
