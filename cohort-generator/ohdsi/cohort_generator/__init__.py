from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import ListVector, StrSexpVector
from rpy2.robjects.packages import importr

cohort_generator = importr('CohortGenerator')


class CohortTables:

    @staticmethod
    def get_cohort_table_names(
        cohort_table: str = "cohort",
        cohort_inclusion_table: str | None = None,
        cohort_inclusion_result_table: str | None = None,
        cohort_inclusion_stats_table: str | None = None,
        cohort_summary_stats_table: str | None = None,
        cohort_censor_stats_table: str | None = None
    ) -> ListVector:
        """
        Get the names of the cohort tables.
        """
        args = {
            "cohortTable": cohort_table,
            "cohortInclusionTable": cohort_inclusion_table,
            "cohortInclusionResultTable": cohort_inclusion_result_table,
            "cohortInclusionStatsTable": cohort_inclusion_stats_table,
            "cohortSummaryStatsTable": cohort_summary_stats_table,
            "cohortCensorStatsTable": cohort_censor_stats_table
        }
        # remove None values
        args = {k: v for k, v in args.items() if v is not None}
        return cohort_generator.getCohortTableNames(**args)

    @staticmethod
    def create_cohort_tables(
        cohort_database_schema: str,
        connection_details: ListVector | None = None,
        connection: RS4 | None = None,
        cohort_table_names: ListVector | None = None,
        incremental: bool = False
    ) -> RS4:
        """
        Create cohort tables.

        Creates the cohort tables in the database.

        Parameters
        ----------
        cohort_database_schema : str
            The schema to create the cohort tables in
        connection_details : ListVector, optional
            The connection details, by default None
        connection : RS4, optional
            The connection, by default None
        cohort_table_names : ListVector, optional
            The names of the cohort tables, by default None
        incremental : bool, optional
            A boolean representing if the tables should be created
            incrementally, by default False

        Returns
        -------
        RS4
            A wrapped cohort generation R object
        """
        if cohort_table_names is None:
            cohort_table_names = CohortTables.get_cohort_table_names()

        args = {
            "cohortDatabaseSchema": cohort_database_schema,
            "connectionDetails": connection_details,
            "connection": connection,
            "cohortTableNames": cohort_table_names,
            "incremental": incremental
        }
        # remove None values
        args = {k: v for k, v in args.items() if v is not None}
        return cohort_generator.createCohortTables(**args)
