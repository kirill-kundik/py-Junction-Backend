from connexion import NoContent

import app
from app.db.models import WishList
from app.db.exceptions import DatabaseException


def create(wishlist_item):
    item = app.db.add_wish_list_item(WishList(**wishlist_item))
    return item.dump()


def delete(item_id):
    try:
        app.db.delete_wish_list_item(app.db.get_wish_list_item(item_id))
    except DatabaseException:
        return NoContent, 404
    return NoContent, 200


def get_all(from_user):
    items = app.db.get_user_wish_list(from_user["id"])
    return [item.dump() for item in items]
