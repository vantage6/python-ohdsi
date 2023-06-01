import json

from rpy2 import robjects
from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import StrVector

from rpy2.robjects.packages import importr


#
# Converters
#
@robjects.default_converter.py2rpy.register(type(None))
def _py_none_to_null(py_obj):
    return robjects.NULL


#
# R interface
#
circe_r = importr('CirceR')


#
# Python wrappers
#
class CohortExpression:

    @staticmethod
    def cohort_expression_from_json(expression_json: str | dict) -> RS4:
        """
        Render read JSON into a R CohortExpression instance.

        Reads a String (json) and deserializes it into a
        org.ohdsi.circe.cohortdefinition.CohortExpression as the R library
        is a wrapper around the Java library.

        Parameters
        ----------
        expression_json : str | dict
            A JSON ``str`` or a ``dict`` representing a cohort expression

        Returns
        -------
        RS4
            A wrapped cohort expression R object
        """
        if isinstance(expression_json, dict):
            expression_json = json.dumps(expression_json)
        return circe_r.cohortExpressionFromJson(expression_json)


class CohortSqlBuilder:

    @staticmethod
    def create_generate_options(
        cohort_id_field_name: str = None, cohort_id: int = None,
        cdm_schema: str = None, target_table: str = None,
        result_schema: str = None, vocabulary_schema: str = None,
        generate_stats: bool = None
    ) -> RS4:
        """
        Create Generation Options.

        Creates the generation options object for use in
        ``build_cohort_query``

        Parameters
        ----------
        cohort_id_field_name : str, optional
            The field that contains the cohortId in the cohort table, by
            default None
        cohort_id : int, optional
            The generated cohort ID, by default None
        cdm_schema : str, optional
            The value of the CDM schema, by default None
        target_table : str, optional
            The cohort table name, by default None
        result_schema : str, optional
            The schema the cohort table belongs to, by default None
        vocabulary_schema : str, optional
            The schema of the vocabulary tables (defaults to cdmSchema),
            by default None
        generate_stats : bool, optional
            A boolean representing if the query should include inclusion rule
            statistics calculation, by default None

        Returns
        -------
        RS4
            A wrapped generation options R object
        """
        kwargs = {
            'cohortIdFieldName': cohort_id_field_name, 'cohortId': cohort_id,
            'cdmSchema': cdm_schema, 'targetTable': target_table,
            'resultSchema': result_schema,
            'vocabularySchema': vocabulary_schema,
            'generateStats': generate_stats
        }
        # filter out None values, R does not want those
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return circe_r.createGenerateOptions(**kwargs)

    @staticmethod
    def build_cohort_query(cohort_expression: RS4, options: RS4 = None) \
            -> StrVector:
        """
        Build Cohort SQL

        Generates the OMOP CDM Sql to generate the cohort expression.

        Parameters
        ----------
        cohort_expression : RS4 | str
            An R object or a JSON string containing the cohort expression
        options : RS4, optional
            The options object from ``create_generate_options``, by default
            None

        Returns
        -------
        StrVector
            contains the SQL statements
        """
        return circe_r.buildCohortQuery(cohort_expression, options)


class ConceptSetExpression:

    @staticmethod
    def concept_set_expression_from_json(expression_json: str | dict) \
            -> RS4:
        """
        Read JSON into a ConceptSetExpression instance.

        Reads a String (json) and deserializes it into a
        ``org.ohdsi.circe.vocabulary.ConceptSetExpression`` as the R library
        is a wrapper around the Java library.

        Parameters
        ----------
        concept_set : str | dict
            A JSON ``str`` or a ``dict`` representing a concept set expression

        Returns
        -------
        RS4
            A wrapped concept set expression R object
        """
        if isinstance(expression_json, dict):
            expression_json = json.dumps(expression_json)
        return circe_r.conceptSetExpressionFromJson(expression_json)


class ConceptSetSqlBuilder:

    @staticmethod
    def build_concept_set_query(concept_set_expression: str | dict) \
            -> StrVector:
        """
        Generates the OMOP CDM Sql to resolve the concept set expression

        Parameters
        ----------
        concept_set_expression : str | dict
            a string containing the JSON for the conceptset expression.

        Returns
        -------
        StrVector
            OHDSI Sql for the conceptset expression
        """
        if isinstance(concept_set_expression, dict):
            concept_set_expression = json.dumps(concept_set_expression)
        return circe_r.buildConceptSetQuery(concept_set_expression)


class PrintFriendly:

    @staticmethod
    def cohort_print_friendly(expression: RS4 | dict | str) -> StrVector:
        """
        Create a print friendly version of a cohort expression.

        Parameters
        ----------
        expression : RS4 | dict | str
            A str, dict or result of ``cohort_expression_from_json``
            containing the cohort expression.

        Returns
        -------
        StrVector
            A character vector containing the print friendly version of the
            cohort expression.
        """
        if isinstance(expression, dict):
            expression = json.dumps(expression)
        return circe_r.cohortPrintFriendly(expression)

    @staticmethod
    def concept_set_print_friendly(concept_set: str | dict) -> StrVector:
        """
        Create a print friendly version of a concept set expression.

        Parameters
        ----------
        expression : str | json
            A JSON ``str`` or a ``dict`` representing a concept set

        Returns
        -------
        StrVector
            A character vector containing the print friendly version of the
            concept set expression.
        """
        if isinstance(concept_set, dict):
            concept_set = json.dumps(concept_set)
        return circe_r.conceptSetPrintFriendly(concept_set)

    @staticmethod
    def concept_set_list_print_friendly(concept_set_list: str | dict) \
            -> StrVector:
        """
        Render conceptSet array for print-friendly

        Generates a print-friendly (human-readable) representation of an array
        of concept sets. This can for example be used in a study protocol.

        Parameters
        ----------
        expression : str | dict
            A JSON ``str`` or a ``dict`` representing a concept set list

        Returns
        -------
        StrVector
            A character vector containing the print friendly version of the
            concept set expression.
        """
        if isinstance(concept_set_list, dict):
            concept_set_list = json.dumps(concept_set_list)
        return circe_r.conceptSetListPrintFriendly(concept_set_list)
