#
# File to test basic functionality of circe
#

import json

from importlib.resources import files

from ohdsi.circe import (
    cohort_expression_from_json,
    build_cohort_query,
    concept_set_expression_from_json,
    build_concept_set_query,
    cohort_print_friendly,
    concept_set_print_friendly,
    concept_set_list_print_friendly,
    create_generate_options
)

f_ = files('ohdsi.circe.data')
cohort_json = files('ohdsi.circe.data').joinpath('simpleCohort.json')\
    .read_text()
concept_set_json = files('ohdsi.circe.data').joinpath('conceptSet.json')\
    .read_text()
concept_set_list_json = files('ohdsi.circe.data')\
    .joinpath('conceptSetList.json').read_text()

cohort = cohort_expression_from_json(cohort_json)
options = create_generate_options()
sql = build_cohort_query(cohort, options)
print(sql)

concept_json = json.loads(concept_set_json)

concept_set_expression = concept_set_expression_from_json(
    concept_json['expression']
)
print(concept_set_expression)

concept_set_sql = build_concept_set_query(
    concept_json['expression']
)
print(concept_set_sql)

print("***")
print(cohort_print_friendly(cohort))
print(cohort_print_friendly(cohort_json))
print(concept_set_print_friendly(concept_set_json))
print(concept_set_list_print_friendly(concept_set_list_json))