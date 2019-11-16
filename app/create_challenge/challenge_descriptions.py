import random


def get_random_description():
    descriptions = []
    rand_index = random.randint(0, len(descriptions))
    return descriptions[rand_index]
