import datetime

import app
from app.db.models import Challenge, ChallengeDifficulty, Item, PeriodType, User
from .challenge_descriptions import get_random_description, get_random_short_description


def get_parts_count_by_sub_category(period: PeriodType) -> (int, int):
    """
    :param period: time period of item category
    :return: number of the current period parts in consequent period
    """
    return {
        PeriodType.daily.value: (7, 7),  # one week has 7 days
        PeriodType.weekly.value: (4, 28)  # one month has 4 weeks
    }[period.value]


def create_challenge_on_item_add(item: Item):
    user: User = app.db.get_user_by_id(item.user_fk)
    period = item.sub_category.period
    parts_count, number_of_days = get_parts_count_by_sub_category(period)
    start_day = datetime.datetime.today() - datetime.timedelta(days=number_of_days)
    period_expense_sum = app.db.get_user_items_sum_by_period(user.id, start_day)
    save_amount = period_expense_sum / parts_count
    name = f"Save on your {item.name}!"
    challenge = Challenge(name=name,
                          full_description=get_random_description(item.sub_category.name),
                          brief_description=get_random_short_description(),
                          earn_amount=float(str(f"{save_amount:.2f}")),
                          difficulty=ChallengeDifficulty.easy,
                          sub_category_fk=item.sub_category.id)
    app.db.add_challenge(challenge)
    app.db.add_user_recommended_challenge(user.id, challenge.id)
    # user.recommended_challenges.append(app.db.get_challenge_by_id(challenge.id))
    # app.db.update_user(user)


# if __name__ == "__main__":
#     for item in app.db.get_user_items(1):
#         print(item.name)
#         create_challenge_on_item_add(item)
