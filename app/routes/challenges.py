from connexion import NoContent

import app
from app.db.exceptions import DatabaseException
from app.db.models import User


def get_all(from_user):
    challenges = app.db.get_challenges_by_user(from_user["id"])
    applied_challenges_id = [challenge.id for challenge in challenges]
    recommended_challenges = app.db.get_recommended_challenges_by_user(from_user["id"])

    return [{**challenge.dump(), "applied": True} for challenge in challenges] + \
           [challenge.dump() for challenge in recommended_challenges if challenge.id not in applied_challenges_id]


def apply(challenge_id, from_user):
    try:
        user: User = app.db.get_user_by_id(from_user["id"])
        user.challenges.append(app.db.get_challenge_by_id(challenge_id))
        app.db.update_user(user)
    except DatabaseException as e:
        return e, 404
    return NoContent, 200


def unapply(challenge_id, from_user):
    try:
        app.db.unapply_user(from_user["id"], challenge_id)
    except DatabaseException:
        return NoContent, 404
    return NoContent, 200
