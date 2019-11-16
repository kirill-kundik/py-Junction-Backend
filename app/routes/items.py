from connexion import NoContent

import app
from app.db.models import Item
from app.db.exceptions import DatabaseException


def get_all(from_user):
    items = app.db.get_user_items(from_user["id"])

    return [item.drop() for item in items]


def create(item):
    try:
        app.db.add_item(Item(**item))
    except DatabaseException:
        return NoContent, 404
    return NoContent, 200
