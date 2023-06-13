from rpy2 import robjects
from rpy2.robjects.packages import importr
from importlib.resources import files

from circe.cohort_expression import cohort_expression_from_json
from circe.cohort_sql_builder import build_cohort_query


cohort_json = files('circe.data').joinpath('simpleCohort.json').read_text()

print("importing R cohort generator")
ch = importr('CohortGenerator')

cohort_to_create = ch.createEmptyCohortDefinitionSet()

# circe
cohort = cohort_expression_from_json(cohort_json)
sql = build_cohort_query(cohort)
##

cohort_table_names = ch.getCohortTableNames(cohortTable = "my_cohort_table")

print("importing R eunomia")
eunomia = importr('Eunomia')
eunomia.getEunomiaConnectionDetails()

conectionDetails = eunomia.getEunomiaConnectionDetails()
ch.createCohortTables(connectionDetails=conectionDetails, cohortDatabaseSchema = "main", cohortTableNames =cohort_table_names)




rbase = importr('base')
cohorts_to_create2 = rbase.rbind(
    cohort_to_create,
    robjects.r('data.frame')(cohortId=1, cohortName="SimpleCohort", sql=str(sql), stringAsFactors=False)
)

cohortGenerated = ch.generateCohortSet(
    connectionDetails=conectionDetails,
    cdmDatabaseSchema="main",
    cohortDatabaseSchema="main",
    cohortTableNames=cohort_table_names,
    cohortDefinitionSet=cohorts_to_create2
)


counts = ch.getCohortCounts(
    connectionDetails=conectionDetails,
    cohortDatabaseSchema = "main",
    cohortTable=cohort_table_names.rx2("cohortTable")
)

# from rpy2.robjects import pandas2ri
# import rpy2.robjects as ro
# import pandas as pd
# with (ro.default_converter + pandas2ri.converter).context():
#     pd_from_r_df = ro.conversion.get_conversion().rpy2py(cohortGenerated)
