import app


def get_pie_chart_data(from_user):
    return app.db.get_pie_chart_data(from_user["id"])


def get_line_chart_data(from_user):
    months, values = app.db.get_bar_chart_data(
        from_user["id"], from_user.get("sub_category_id", None),
        from_user.get("category_id", None)
    )
    return [months, values]
