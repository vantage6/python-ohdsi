import time
import logging
import sys
import os
import io
import pickle
import codecs
import rpy2.robjects as ro

from contextlib import redirect_stdout

from celery import shared_task, Task, signals
from ohdsi.database_connector import (
    create_connection_details,
    connect,
    query_sql,
    disconnect
)

from ohdsi.feature_extraction import (
    get_db_covariate_data
)

from ohdsi.common import andromeda_to_df
from rpy2.robjects import pandas2ri
# pandas2ri.activate()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

dbms = os.environ['OMOP_DBMS']
server = os.environ['OMOP_SERVER']
database = os.environ['OMOP_DATABASE']
user = os.environ['OMOP_USER']
password = os.environ['OMOP_PASSWORD']
port = os.environ['OMOP_PORT']


class OhdsiTask(Task):

    def __init__(self):
        super().__init__()

        self.log_stream = io.StringIO()
        self.connection = None

        signals.task_prerun.connect(self.on_task_prerun)
        # signals.task_success.connect(self.on_task_success)

    def on_task_prerun(self, task_id, task, *args, **kwargs):
        # self.update_state(state='PROGRESS', meta={'current': 2, 'total': 10})
        log.info("Creating connection details")
        print(dbms, server, user, password, port)
        self.update_state(state='INITIALIZE', meta={'step': 1, 'steps': 5})
        connection_details = create_connection_details(
            dbms, server=f"{server}/{database}", user=user, password=password,
            port=port
        )

        log.info("Connecting to database")
        self.update_state(state='CONNECT', meta={'step': 2, 'steps': 5})
        with redirect_stdout(self.log_stream):
            self.connection = connect(connection_details)

    def on_task_success(self, result, **kwargs):
        log.info("Disconnecting from database")
        #TODO: this part is not returned to the client
        # with redirect_stdout(self.log_stream):
        disconnect(self.connection)


@shared_task(bind=True, ignore_result=False, time_limit=25, base=OhdsiTask)
def background_task(self, a , b):
    log.info("Querying database")
    self.update_state(state='QUERYING')
    result = None
    with redirect_stdout(self.log_stream):
        try:
            result = query_sql(self.connection,
                               "SELECT * FROM omopcdm.person LIMIT 3")
            # FIXME FM 11-9-2023: this should be removed when the python-ohdsi
            # package do this
            with (ro.default_converter + pandas2ri.converter).context():
                result = ro.conversion.get_conversion().rpy2py(result)

        except Exception as e:
            log.exception(e)

    log.info("...Task is done...")
    # FIXME FM 11-9-2023: `default_handler=str` is a workaround as some types
    # in the dataframe are not JSON serializable.
    return result.to_json(default_handler=str)  # {"data": result, "log": self.log_stream.getvalue()}


@shared_task(bind=True, ignore_result=False, time_limit=25)
def background_task2(self, a: int, b: int) -> int:

    # Stream output to log to return some logging to the job initiator
    f = io.StringIO()

    # self.update_state(state='PROGRESS', meta={'current': 2, 'total': 10})
    log.info("Creating connection details")
    self.update_state(state='PROGRESS', meta={'step': 1, 'steps': 5})
    connection_details = create_connection_details(
        dbms, server=f"{server}/{database}", user=user, password=password,
        port=port
    )

    log.info("Connecting to database")
    self.update_state(state='PROGRESS', meta={'step': 2, 'steps': 5})
    with redirect_stdout(f):
        con = connect(connection_details)

    log.info("Querying database")
    self.update_state(state='PROGRESS', meta={'step': 3, 'steps': 5})
    result = None
    with redirect_stdout(f):
        try:
            result = query_sql(con, "SELECT * FROM omopcdm.person LIMIT 3")
        except Exception as e:
            log.exception(e)

    log.info("Preparing result for transport")
    self.update_state(state='PROGRESS', meta={'step': 4, 'steps': 5})
    # TODO: Can we use something else than pickle??
    pickled = codecs.encode(pickle.dumps(result), "base64").decode()

    log.info("Disconnecting from database")
    self.update_state(state='PROGRESS', meta={'step': 5, 'steps': 5})
    with redirect_stdout(f):
        disconnect(con)

    return {"data": pickled, "log": f.getvalue()}
