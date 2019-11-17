import app


def get_pie_chart_data(from_user):
    return app.db.get_pie_chart_data(from_user["id"])
