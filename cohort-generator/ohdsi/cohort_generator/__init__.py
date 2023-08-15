import os

from pathlib import Path

from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import ListVector
from rpy2.robjects.packages import importr

# When building documentation for the project, the following import will fail
# as the package is not installed. In this case, we set the variable to None
# so that the documentation can be built.
if os.environ.get('IGNORE_R_IMPORTS', False):
    cohort_generator = None
    base_r = None
else:
    cohort_generator = importr('CohortGenerator')
    base_r = importr('base')


# -----------------------------------------------------------------------------
# wrapper: CohortGenerator/R/CohortDefinitionSet.R
# functions:
#    - create_empty_cohort_definition_set (createEmptyCohortDefinitionSet)
#    - save_cohort_definition_set (saveCohortDefinitionSet)
# -----------------------------------------------------------------------------
def create_empty_cohort_definition_set(verbose: bool = False) -> RS4:
    """
    Create an empty CohortDefinitionSet object

    Wraps the R ``CohortGenerator::createEmptyCohortDefinitionSet`` function
    defined in ``CohortGenerator/R/CohortDefinitionSet.R``.

    Parameters
    ----------
    verbose : bool, optional
        When True, descriptions of each field in the data frame are
        returned. By default False.
    """
    return cohort_generator.createEmptyCohortDefinitionSet(verbose)


def save_cohort_definition_set(
    cohort_definition_set: RS4,
    settings_file_name: str | Path = "inst/cohorts.csv",
    json_folder: str | Path = "inst/cohorts",
    sql_folder: str | Path = "inst/sql/sql_server",
    cohort_file_name_format: str = "%s",
    cohort_file_name_value: list[str] = ["cohort_id"],
    subset_json_folder: str | Path = "inst/cohort_subset_definitions/",
    verbose: bool = False
) -> None:
    """
    Save the cohort definition set to the file system

    This function saves a cohort_definition_set to the file system and
    provides options for specifying where to write the individual elements:
    the settings file will contain the cohort information as a CSV
    specified by the settingsFileName, the cohort JSON is written to the
    jsonFolder and the SQL is written to the sqlFolder. We also provide a
    way to specify the json/sql file name format using the
    cohort_file_name_format and cohort_file_name_value parameters.

    Wraps the R ``CohortGenerator::saveCohortDefinitionSet`` function
    defined in ``CohortGenerator/R/CohortDefinitionSet.R``.

    Parameters
    ----------
    cohort_definition_set : RS4
        A CohortDefinitionSet object
    settings_file_name : str, optional
        The name of the CSV file that will hold the cohort information
        including the cohortId and cohortName
    json_folder : str, optional
        The name of the folder that will hold the JSON representation
        of the cohort if it is available in the cohortDefinitionSet
    sql_folder : str, optional
        The name of the folder that will hold the SQL representation
        of the cohort
    cohort_file_name_format : str, optional
        Defines the format string  for naming the cohort JSON and SQL
        files. The format string follows the standard defined in the base
        ``sprintf`` function.
    cohort_file_name_value : list[str], optional
        Defines the columns in the cohortDefinitionSet to use in
        conjunction with the cohortFileNameFormat parameter
    subset_json_folder : str, optional
        Defines the folder to store the subset JSON
    verbose : bool, optional
        When TRUE, logging messages are emitted to indicate export
        progress. By default False.
    """
    return cohort_generator.saveCohortDefinitionSet(
        cohort_definition_set, settings_file_name, json_folder, sql_folder,
        cohort_file_name_format, cohort_file_name_value,
        subset_json_folder, verbose
    )


# -----------------------------------------------------------------------------
# wrapper: CohortGenerator/R/CohortConstruction.R
# functions:
#    - generate_cohort_set (generateCohortSet)
# -----------------------------------------------------------------------------
def generate_cohort_set(
    cdm_database_schema: str,
    cohort_definition_set: RS4,
    connection_details: ListVector | None = None,
    connection: RS4 | None = None,
    temp_emulation_schema: str | None = None,
    cohort_database_schema: str | None = None,
    cohort_table_names: ListVector | None = None,
    stop_on_error: bool = True,
    incremental: bool = False,
    incremental_folder: str | Path = None
) -> RS4:
    """
    Generate a cohort set

    This function generates a set of cohorts in the cohort table.

    Wraps the R ``CohortGenerator::generateCohortSet`` function defined in
    ``CohortGenerator/R/CohortConstruction.R``.

    Parameters
    ----------
    cdm_database_schema : str
        The schema containing the CDM
    connection_details : ListVector | None, optional
        The connection details obtained using
        ``Connect.create_connection_details(...)``, by default None
    connection : None, optional
        The connection object obtained from ``Connect.connect(...)``, by
        default None
    temp_emulation_schema : None, optional
        The schema to use for temp tables, by default None


    """
    args = {
        "cdmDatabaseSchema": cdm_database_schema,
        "connectionDetails": connection_details,
        "connection": connection,
        "tempEmulationSchema": temp_emulation_schema,
        "cohortDatabaseSchema": cohort_database_schema,
        "cohortTableNames": cohort_table_names,
        "cohortDefinitionSet": cohort_definition_set,
        "stopOnError": stop_on_error,
        "incremental": incremental,
        "incrementalFolder": incremental_folder
    }
    # remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return cohort_generator.generateCohortSet(**args)


# -----------------------------------------------------------------------------
# wrapper: CohortGenerator/R/CohortTables.R
# functions:
#    - get_cohort_table_names (getCohortTableNames)
#    - create_cohort_tables (createCohortTables)
# -----------------------------------------------------------------------------
def get_cohort_table_names(
    cohort_table: str = "cohort",
    cohort_inclusion_table: str | None = None,
    cohort_inclusion_result_table: str | None = None,
    cohort_inclusion_stats_table: str | None = None,
    cohort_summary_stats_table: str | None = None,
    cohort_censor_stats_table: str | None = None
) -> ListVector:
    """
    Get the names of the cohort tables

    Wraps the R ``CohortGenerator::getCohortTableNames`` function defined in
    ``CohortGenerator/R/CohortTables.R``.

    Parameters
    ----------
    cohort_table : str, optional
        The name of the cohort table, by default "cohort"
    cohort_inclusion_table : str, optional
        The name of the cohort inclusion table, by default None
    cohort_inclusion_result_table : str, optional
        The name of the cohort inclusion result table, by default None
    cohort_inclusion_stats_table : str, optional
        The name of the cohort inclusion stats table, by default None
    cohort_summary_stats_table : str, optional
        The name of the cohort summary stats table, by default None
    cohort_censor_stats_table : str, optional
        The name of the cohort censor stats table, by default None

    Returns
    -------
    ListVector
        A list of cohort table names
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


def create_cohort_tables(
    cohort_database_schema: str,
    connection_details: ListVector | None = None,
    connection: RS4 | None = None,
    cohort_table_names: ListVector | None = None,
    incremental: bool = False
) -> RS4:
    """
    Create cohort tables

    Creates the cohort tables in the database.

    Wraps the R ``CohortGenerator::createCohortTables`` function defined in
    ``CohortGenerator/R/CohortTables.R``.

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
        cohort_table_names = get_cohort_table_names()

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


# -----------------------------------------------------------------------------
# wrapper: CohortGenerator/R/CohortCount.R
# functions:
#    - get_cohort_counts (getCohortCounts)
# -----------------------------------------------------------------------------
def get_cohort_counts(
    cohort_database_schema: str,
    connection_details: ListVector | None = None,
    connection: RS4 | None = None,
    cohort_table: str = "cohort",
    cohort_ids: list[int] = [],
    cohort_definition_set: RS4 = None,
    database_id: int | None = None
) -> RS4:
    """
    Get cohort counts.

    Gets the counts for the specified cohort ids.

    Wraps the R ``CohortGenerator::getCohortCounts`` function defined in
    ``CohortGenerator/R/CohortCount.R``.

    Parameters
    ----------
    cohort_database_schema : str
        The schema containing the cohort tables
    connection_details : ListVector, optional
        The connection details, by default None
    connection : RS4, optional
        The connection, by default None
    cohort_table : str, optional
        The name of the cohort table, by default "cohort"
    cohort_ids : list[int], optional
        The cohort ids to get the counts for, by default []
    cohort_definition_set : RS4, optional
        The cohort definition set, by default None
    database_id : str, optional
        The database id, by default None

    Returns
    -------
    RS4
        A wrapped cohort counts R object
    """
    args = {
        "cohortDatabaseSchema": cohort_database_schema,
        "connectionDetails": connection_details,
        "connection": connection,
        "cohortTable": cohort_table,
        "cohortIds": cohort_ids,
        "cohortDefinitionSet": cohort_definition_set,
        "databaseId": database_id
    }
    # remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return cohort_generator.getCohortCounts(**args)
