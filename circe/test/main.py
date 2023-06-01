from importlib.resources import files

from ohdsi.circe import CohortExpression
from ohdsi.circe import CohortSqlBuilder

f_ = files('ohdsi.circe.data')
cohort_json = files('ohdsi.circe.data').joinpath('simpleCohort.json').read_text()
cohort = CohortExpression.cohort_expression_from_json(cohort_json)
sql = CohortSqlBuilder.build_cohort_query(cohort, None)