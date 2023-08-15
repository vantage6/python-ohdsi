import os

from flask import Flask
from flask_restful import Api
from celery import Celery

from .resource import FeatureExtraction, FeatureExtractionJob

broker_url = os.environ["CELERY_BROKER_URL"] or \
    "amqp://guest:guest@127.0.0.1:5672"
backend_url = os.environ["CELERY_RESULT_BACKEND"] or \
    "db+sqlite:///results.sqlite"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project1.db"

app.config["CELERY"] = dict(
    broker=broker_url,
    result_backend=backend_url,
    task_ignore_result=True,
)

api = Api(app)

api.add_resource(FeatureExtraction, "/feature-extraction")
api.add_resource(FeatureExtractionJob,
                 "/feature-extraction/<string:job_id>")


# class FlaskTask(Task):
#     def __call__(self, *args: object, **kwargs: object) -> object:
#         with app.app_context():
#             return self.run(*args, **kwargs)


celery_app = Celery(app.name)
celery_app.config_from_object(app.config["CELERY"])
celery_app.set_default()
# celery_app.Task = FlaskTask
