from connexion import NoContent

import app
from app.db.models import Item
from app.db.exceptions import DatabaseException


def get_all(from_user):
    items = app.db.get_user_items(from_user["id"])

    return [item.dump() for item in items]


def create(item):
    try:
        new_item = Item(**item)
        app.db.add_item(new_item)
    except DatabaseException:
        return NoContent, 404
    return new_item.dump()
