from rpy2.robjects.packages import importr

# from ohdsi.circe.convert import conversion_rules
import ohdsi.circe.convert

# reference to the R package
circe_r = importr('CirceR')


class CohortExpression:

    @staticmethod
    def cohort_expression_from_json(expression_json):
        return circe_r.cohortExpressionFromJson(expression_json)


class CohortSqlBuilder:

    @staticmethod
    def create_generate_options(cohort_id_field_name, cohort_id, cdm_schema,
                                target_table, result_schema, vocabulary_schema,
                                generate_stats):
        return circe_r.createGenerateOptions(
            cohort_id_field_name, cohort_id, cdm_schema, target_table,
            result_schema, vocabulary_schema, generate_stats
        )

    @staticmethod
    def build_cohort_query(cohort_expression, options):
        return circe_r.buildCohortQuery(cohort_expression, options)


class ConceptSetExpression:

    @staticmethod
    def concept_set_expression_from_json(expression_json):
        return circe_r.conceptSetExpressionFromJson(expression_json)


class ConceptSetSqlBuilder:

    @staticmethod
    def build_concept_set_query(concept_set_expression, options):
        return circe_r.buildConceptSetQuery(concept_set_expression, options)


class PrintFriendly:

    @staticmethod
    def cohort_print_friendly(expression):
        return circe_r.cohortPrintFriendly(expression)

    @staticmethod
    def concept_set_list_print_friendly(concept_set_list):
        return circe_r.conceptSetListPrintFriendly(concept_set_list)

    @staticmethod
    def concept_set_print_friendly(concept_set):
        return circe_r.conceptSetPrintFriendly(concept_set)