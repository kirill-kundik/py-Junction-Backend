import app


def get_all():
    return [subcategory.dump() for subcategory in app.db.get_all_subcategories()]
