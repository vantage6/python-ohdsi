from kombu.exceptions import OperationalError
from celery.result import AsyncResult
from flask_restful import Resource

from http import HTTPStatus
from flask import jsonify

from .task import background_task


def is_worker_awake(app):
    # TODO: use ping
    insp = app.control.inspect()
    nodes = insp.stats()
    if not nodes:
        return False
    return True


class FeatureExtractionJob(Resource):

    def get(self, job_id: str) -> dict:
        """
        Obtain Feature Extraction results for a given job id.

        Parameters
        ----------
        job_id : int
            The job id to obtain results for.

        Returns
        -------
        dict
            The results of the Feature Extraction job.
        """
        result = AsyncResult(job_id)

        if result.ready():
            res = result.result
        else:
            res = None

        if not isinstance(res, str | dict):
            res = str(res)
            print('not a sting')
            print(res)
        else:
            print('is a string')

        return jsonify({
            "id": job_id,
            "state": result.state,
            "value": res,
            "worker_available": is_worker_awake(result.app),
            "info": str(result.info),
        })


class FeatureExtraction(Resource):

    def post(self):

        try:
            task: AsyncResult = background_task.delay(1, 2)
        except OperationalError:
            return {"error": "Celery is not available"}, \
                HTTPStatus.SERVICE_UNAVAILABLE

        return {"id": task.id}
