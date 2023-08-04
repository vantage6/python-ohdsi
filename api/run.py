import logging
from src import app
# import os

# from flask import Flask
# from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy

# from ohdsi.database_connector import Connect, Sql
# from ohdsi.feature_extraction import GetCovariates, DetailedCovariateSettings

# from rpy2.robjects import conversion, default_converter

# from .src.resource import FeatureExtraction

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Initialization
# db = SQLAlchemy()
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# db.init_app(app)
# api = Api(app)


# FeatureExtraction(api)

# TODO: this should return a job id, from which the algorithm can collect the
# result at a later point
# @app.route("/feature-extraction")
# def feature_extraction():

#     with conversion.localconverter(default_converter):

#         logger.info("Feature Extraction")

#         # TODO - move this to a config file
#         driver = os.environ.get("DB_DRIVER", "postgresql")
#         user = os.environ.get("POSTGRES_USER", "postgres")
#         password = os.environ.get("POSTGRES_PASSWORD", "matchstick-wrapper-sliding-bulb")
#         host = os.environ.get("POSTGRES_HOST", "localhost")
#         port = os.environ.get("POSTGRES_PORT", 5432)
#         database = os.environ.get("POSTGRES_DATABASE", "postgres")

#         connection_details = Connect.create_connection_details(
#             driver,
#             server=f"{host}/{database}",
#             user=user,
#             password=password,
#             port=port,
#         )

#         logger.info(driver)
#         logger.info(user)
#         logger.info(password)
#         logger.info(host)
#         logger.info(port)
#         logger.info(database)

#         try:
#             # settings = \
#             #     DetailedCovariateSettings.create_default_covariate_settings()
#             connection = Connect.connect(connection_details)
#             logger.info("Feature Extraction1")
#             res = Sql.query_sql(connection, "SELECT * FROM omopcdm.condition_era")
#             logger.info("Feature Extraction2")
#             print(res)
#             logger.info("Feature Extraction3")
#             # data = GetCovariates.get_db_covariate_data(
#             #     cdm_database_schema="omopcdm",
#             #     connection=connection,
#             #     cohort_database_schema="results",
#             #     cohort_table="cohort",
#             #     covariate_settings=settings,
#             # )
#             Connect.disconnect(connection)


#         except Exception as e:
#             logger.info("Feature Extraction4")
#             logger.exception(e)
#         logger.info("Feature Extraction Complete")
#         return "done"


# @app.route("/cohort-generator")
# def cohort_generator():
#     logger.info("Cohort Generator")
#     return "Cohort Generator"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
