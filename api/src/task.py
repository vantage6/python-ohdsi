import time
import logging
import sys
import os
import io
import pickle
import codecs

from contextlib import redirect_stdout

from celery import shared_task
from ohdsi.database_connector import (
    create_connection_details,
    connect,
    query_sql
)

log = logging.getLogger(__name__)

@shared_task(bind=True, ignore_result=False, time_limit=25)
def background_task(self, a: int, b: int) -> int:
    # capture = StringIO()
    # sys.stdout = capture
    sys.stdout.write("Hello from background task")
    self.update_state(state='PROGRESS', meta={'current': 1, 'total': 10})
    log.debug("Sleeping for 10 seconds")
    print("Sleeping for 11 seconds")
    self.update_state(state='PROGRESS', meta={'current': 2, 'total': 10})
    connection_details = create_connection_details(
        "postgresql",
        server="host.docker.internal/postgres",
        user="postgres",
        password="matchstick-wrapper-sliding-bulb",
        port=5454
    )
    # find the freeze of the current python environment
    # stream = os.popen('pip freeze')
    # output = stream.read()
    # print(output)

    self.update_state(state='PROGRESS', meta={'current': 11, 'total': 10})
    f = io.StringIO()

    with redirect_stdout(f):
        con = connect(connection_details)

    # print(con)
    self.update_state(state='PROGRESS', meta={'current': 3, 'total': 10})
    result = None
    with redirect_stdout(f):
        try:
            result = query_sql(con, "SELECT * FROM omopcdm.person LIMIT 3")
        except Exception as e:
            log.exception(e)

    # print(result)
    print('done here!')
    self.update_state(state='PROGRESS', meta={'current': 4, 'total': 10})
    log.info("Ready!")
    pickled = codecs.encode(pickle.dumps(result), "base64").decode()

    return {
        "data": pickled,
        "log": f.getvalue()
    }
