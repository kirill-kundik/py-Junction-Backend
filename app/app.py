import connexion

import app

config = app.Config
db = app.Database()
flask_app = connexion.App(config.FLASK_APP, specification_dir=app.PROJECT_ROOT.parent / 'api/')
flask_app.add_api('swagger.yaml', base_path='/1.0')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = flask_app.app
