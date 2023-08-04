from . import App

flask_app = App().app
celery_app = flask_app.extensions["celery"]
celery_app.set_default()


print(flask_app)