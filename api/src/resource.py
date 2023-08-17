from kombu.exceptions import OperationalError
from celery.result import AsyncResult
from flask_restful import Resource

from http import HTTPStatus
from flask import jsonify

from .task import background_task


def is_worker_awake(app):
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
        return jsonify({
            "id": job_id,
            "state": result.state,
            "value": result.result if result.ready() else None,
            "worker_available": is_worker_awake(result.app),
            "info": result.info,
        })


class FeatureExtraction(Resource):

    def post(self):

        try:
            task: AsyncResult = background_task.apply_async((1, 2))
        except OperationalError:
            return {"error": "Celery is not available"}, \
                HTTPStatus.SERVICE_UNAVAILABLE

        return {"id": task.id}
