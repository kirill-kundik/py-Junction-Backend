from connexion import NoContent

import app
from app.db.exceptions import DatabaseException


def get_all(from_user):
    challenges = app.db.get_challenges_by_user(from_user["id"])
    applied_challenges_id = [challenge.id for challenge in challenges]
    recommended_challenges = app.db.get_recommended_challenges_by_user(from_user["id"])

    response = [{**challenge.dump(), "applied": True,
                 **app.db.generate_challenge_progress(from_user["id"], challenge.id)} for challenge in challenges] + \
               [challenge.dump() for challenge in recommended_challenges if challenge.id not in applied_challenges_id]
    return [{
        **item,
        "wishlist": [i.dump() for i in app.db.get_wish_list_by_user_and_challenge(item["id"], from_user["id"])]
    } for item in response]


def apply(challenge_id, from_user):
    try:
        app.db.apply_user(from_user["id"], challenge_id, from_user["wishlist_id"])
    except DatabaseException:
        return NoContent, 404
    return {
        **app.db.get_challenge_by_id(challenge_id).dump(),
        "applied": True,
        **app.db.generate_challenge_progress(from_user["id"], challenge_id),
        "wishlist": [item.dump() for item in app.db.get_wish_list_by_user_and_challenge(challenge_id, from_user["id"])]
    }


def unapply(challenge_id, from_user):
    try:
        app.db.unapply_user(from_user["id"], challenge_id)
    except DatabaseException:
        return NoContent, 404
    return {**app.db.get_challenge_by_id(challenge_id).dump(), "applied": False}
