from connexion import NoContent

import app
import random
from app.create_challenge.create_challenge import create_challenge_on_item_add
from app.db.exceptions import DatabaseException
from app.db.models import Item


def get_all(from_user):
    items = app.db.get_user_items(from_user["id"])

    return [item.dump() for item in items]


def create(item):
    try:
        app.db.add_item(Item(**item))
        if random.randint(0, 10) < 3:
            create_challenge_on_item_add(item)
    except DatabaseException:
        return NoContent, 404
    return NoContent, 200
