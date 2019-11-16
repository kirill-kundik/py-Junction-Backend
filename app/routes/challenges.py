from connexion import NoContent

import app
from app.db.exceptions import DatabaseException


def get_all(from_user):
    challenges = app.db.get_challenges_by_user(from_user["id"])
    applied_challenges_id = [challenge.id for challenge in challenges]
    recommended_challenges = app.db.get_recommended_challenges_by_user(from_user["id"])

    return [{**challenge.dump(), "applied": True} for challenge in challenges] + \
           [challenge.dump() for challenge in recommended_challenges if challenge.id not in applied_challenges_id]


def apply(challenge_id, from_user):
    try:
        app.db.apply_user(from_user["id"], challenge_id, from_user["wishlist_id"])
    except DatabaseException:
        return NoContent, 404
    return {**app.db.get_challenge_by_id(challenge_id).dump(), "applied": True}


def unapply(challenge_id, from_user):
    try:
        app.db.unapply_user(from_user["id"], challenge_id)
    except DatabaseException:
        return NoContent, 404
    return {**app.db.get_challenge_by_id(challenge_id).dump(), "applied": False}
