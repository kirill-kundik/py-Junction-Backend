import app


def get_all(from_user):
    challenges = app.db.get_challenges_by_user(from_user["id"])

    return [challenge.dump() for challenge in challenges]


def apply():
    pass
