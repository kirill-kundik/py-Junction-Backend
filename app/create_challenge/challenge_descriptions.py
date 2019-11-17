import random


def get_random_description(subcategory_name: str) -> str:
    descriptions = [f"It's a great time to challenge yourself a bit. "
                    f"We detected that you spend a lot on {subcategory_name}. "
                    f"Maybe it's a good idea to cut costs on that? "
                    f"Accept our challenge, and save your budget!",
                    f"It's never too late to put you into a challenge! "
                    f"So we have one just for you. "
                    f"We have detected your high spending on {subcategory_name}. "
                    f"And we think you may change it. "
                    f"Accept the challenge and save money for something nice! "]
    rand_index = random.randint(0, len(descriptions) - 1)
    return descriptions[rand_index]


def get_random_short_description() -> str:
    descriptions = ["Save your money for something you wish to buy!",
                    "Help yourself to become financially healthier by completing this challenge!",
                    "Don't hesitate to challenge yourself!"]
    rand_index = random.randint(0, len(descriptions) - 1)
    return descriptions[rand_index]
