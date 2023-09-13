import os

from pathlib import Path

from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import ListVector
from rpy2.robjects.packages import importr

from ohdsi.common import ListVectorExtended, to_lower_camel_case
from ohdsi import cohort_generator


# When building documentation for the project, the following import will fail
# as the package is not installed. In this case, we set the variable to None
# so that the documentation can be built.
if os.environ.get('IGNORE_R_IMPORTS', False):
    cohort_diagnostics = None
    base_r = None
else:
    cohort_diagnostics = importr('CohortDiagnostics')
    base_r = importr('base')


# -----------------------------------------------------------------------------
# wrapper: CohortDiagnostics/R/RunDiagnostics.R
# functions:
#    - get_default_covariate_settings (getDefaultCovariateSettings)
#    - execute_diagnostics (executeDiagnostics)
# -----------------------------------------------------------------------------
def get_default_covariate_settings() -> ListVectorExtended:
    """
    Get default covariate settings

    Default covariate settings for cohort diagnostics execution.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.
    """
    return ListVectorExtended.from_list_vector(
        cohort_diagnostics.getDefaultCovariateSettings())

def execute_diagnostics(
        cohort_definition_set: RS4,
        database_id: str,
        cohort_database_schema: str,
        cdm_database_schema: str,
        export_folder: str | None = None,
        database_name: str | None = None,
        database_description: str | None = None,
        connection_details: ListVector | None = None,
        connection: RS4 | None = None,
        temp_emulation_schema: str | None = None,
        cohort_table: str = "cohort",
        cohort_table_names: ListVector | None = None,
        vocabulary_database_schema: str | None = None,
        cohort_ids: list[int] = [],
        cdm_version: int = 5,
        run_inclusion_statistics: bool = True,
        run_included_source_concepts: bool = True,
        run_orphan_concepts: bool = True,
        run_time_series: bool = False,
        run_visit_context: bool = True,
        run_breakdown_index_events: bool = True,
        run_incidence_rate: bool = True,
        run_cohort_relationship: bool = True,
        run_temporal_cohort_characterization: bool = True,
        temporal_covariate_settings: ListVector | ListVectorExtended | None = None,
        min_cell_count: int = 5,
        min_characterization_mean: int = 0.01,
        ir_washout_period: int = 0,
        incremental: bool = False,
        incremental_folder: str | None = None) -> RS4:
    """
    Execute cohort diagnostics

    Runs the cohort diagnostics on all (or a subset of) the cohorts 
    instantiated using the CohortGenerator package.

    Parameters
    ----------
    cohort_definition_set : RS4
        Data.frame of cohorts must include columns cohortId, cohortName, json, 
        sql.
    database_id : str
        A short string for identifying the database (e.g. 'Synpuf').
    cohort_database_schema : str
        The database schema containing the cohort tables.
    cdm_database_schema : str
        The database schema containing the OMOP CDM.
    export_folder : str, optional
        The folder where the output will be exported to. If this folder does 
        not exist it will be created.
    database_name : str, optional
        The full name of the database. If NULL, defaults to value in 
        cdm_source table.
    database_description : str, optional
        A short description (several sentences) of the database. If NULL, 
        defaults to value in cdm_source table.
    connection_details : ListVector | None, optional
        The connection details obtained using
        ``Connect.create_connection_details(...)``, by default None
    connection : None, optional
        The connection object obtained from ``Connect.connect(...)``, by
        default None
    temp_emulation_schema : None, optional
        The schema to use for temp tables, by default None.
    cohort_table : str, optional
        The name of the cohort table, by default "cohort".
    cohort_table_names : ListVector, optional
        The names of the cohort tables, by default None.
    vocabulary_database_schema : str, optional
        The database schema containing the vocabulary, by default set to 
        cdm_database_schema.
    cohort_ids : list(), optional
        A subset of cohort IDs to restrict the diagnostics to.
    cdm_version : int, optional
        Define the OMOP CDM version used: currently supported is "5".
    run_inclusion_statistics : bool, optional
        Generate and export statistic on the cohort inclusion rules?
    run_included_source_concepts : bool, optional
        Generate and export the source concepts included in the cohorts?
    run_orphan_concepts : bool, optional
        Generate and export potential orphan concepts?
    run_time_series : bool, optional
        Generate and export the time series diagnostics?
    run_visit_context : bool, optional
        Generate and export index-date visit context?
    run_breakdown_index_events : bool, optional
        Generate and export the breakdown of index events?
    run_incidence_rate : bool, optional
        Generate and export the cohort incidence  rates?
    run_cohort_relationship : bool, optional
        Generate and export the cohort relationship? Cohort relationship checks 
        the temporal relationship between two or more cohorts.
    run_temporal_cohort_characterization : bool, optional
        Generate and export the temporal cohort characterization? Only records 
        with values greater than 0.001 are returned.
    temporal_covariate_settings : ListVector, optional
        Either an object of type \code{covariateSettings} as created using one 
        of the createTemporalCovariateSettings function in the 
        FeatureExtraction package, or a list of such objects.
    min_cell_count : int, optional
        The minimum cell count for fields contains person counts or fractions.
    min_characterization_mean : int, optional
        The minimum mean value for characterization output. Values below this 
        will be cut off from output. This will help reduce the file size of the 
        characterization output, but will remove information on covariates that 
        have very low values. The default is 0.001 (i.e. 0.1 percent)
    ir_washout_period : int, optional
        Number of days washout to include in calculation of incidence rates,
        default is 0.
    incremental : bool, optional
        Create only cohort diagnostics that haven't been created before?
    incremental_folder : str, optional
        Specify a folder where records are kept of which cohort diagnostics has 
        been executed.
    """

    if not temp_emulation_schema:
        temp_emulation_schema = \
            base_r.getOption("sqlRenderTempEmulationSchema")
        
    if not cohort_table_names:
        cohort_table_names = cohort_generator.get_cohort_table_names(
            cohort_table = cohort_table)

    if not vocabulary_database_schema:
        vocabulary_database_schema = cdm_database_schema

    if not temporal_covariate_settings:
        temporal_covariate_settings = get_default_covariate_settings()
    
    if not incremental_folder:
        incremental_folder = os.path.join(export_folder, "incremental")

    all_arguments = locals()
    all_arguments_camel = {to_lower_camel_case(arg): all_arguments[arg] for arg in all_arguments.keys()}
    
    # remove None values
    args = {k: v for k, v in all_arguments_camel.items() if v is not None}
    return cohort_diagnostics.executeDiagnostics(**args)



# -----------------------------------------------------------------------------
# wrapper: CohortDiagnostics/R/Shiny.R
# functions:
#    - create_merged_results_file (createMergedResultsFile)
#    - launch_diagnostics_explorer (launchDiagnosticsExplorer)
# -----------------------------------------------------------------------------
def create_merged_results_file(
        data_folder: str,
        sqlite_db_path: str = "MergedCohortDiagnosticsData.sqlite",
        overwrite: bool = False,
        table_prefix: str = ""
    ):
    """
    Merge Shiny diagnostics files into sqlite database

    This function combines diagnostics results from one or more databases into 
    a single file. The result is an sqlite database that can be used as input 
    for the Diagnostics Explorer Shiny app.
    
    It also checks whether the results conform to the results data model 
    specifications.

    Parameters
    ----------
    data_folder       
        Folder where the exported zip files for the diagnostics are stored. Use
        the \code{\link{executeDiagnostics}} function to generate these zip 
        files. Zip files containing results from multiple databases may be 
        placed in the same folder.
    sqlite_db_path     
        Output path where sqlite database is placed
    overwrite : bool, optional
        Overwrite existing sqlite lite db if it exists.
    table_prefix : str, optional
        String to insert before table names (e.g. "cd_") for database table 
        names.
    """
    return cohort_diagnostics.createMergedResultsFile(
        data_folder, sqlite_db_path, overwrite, table_prefix)


def launch_diagnostics_explorer(
        sqlite_db_path: str = "MergedCohortDiagnosticsData.sqlite",
        connection_details: RS4 | None = None,
        shiny_config_path: str | None = None,
        results_database_schema: str | None = None,
        vocabulary_database_schema: str | None = None,
        vocabulary_database_schemas: str | None = None,
        table_prefix: str = "",
        cohort_table_name: str = "cohort",
        database_table_name: str = "database",
        about_text: str | None = None,
        run_over_network: bool = False,
        port: int = 80,
        make_publishable: bool = False,
        publish_dir: str | None = None,
        overwrite_publish_dir: bool = False,
        launch_browser: bool = False,
        enable_annotation: bool = True
    ):
    """
    Launch the Diagnostics Explorer Shiny app

    Launches a Shiny app that allows the user to explore the diagnostics

    Parameters
    ----------
#' @param connectionDetails An object of type \code{connectionDetails} as created using the
#'                          \code{\link[DatabaseConnector]{createConnectionDetails}} function in the
#'                          DatabaseConnector package, specifying how to connect to the server where
#'                          the CohortDiagnostics results have been uploaded using the
#'                          \code{\link{uploadResults}} function.
#' @param resultsDatabaseSchema  The schema on the database server where the CohortDiagnostics results
#'                               have been uploaded.
#' @param vocabularyDatabaseSchema (Deprecated) Please use vocabularyDatabaseSchemas.
#' @param vocabularyDatabaseSchemas  (optional) A list of one or more schemas on the database server where the vocabulary tables are located.
#'                                   The default value is the value of the resultsDatabaseSchema. We can provide a list of vocabulary schema
#'                                   that might represent different versions of the OMOP vocabulary tables. It allows us to compare the impact
#'                                   of vocabulary changes on Diagnostics. Not supported with an sqlite database.
#' @param sqliteDbPath     Path to merged sqlite file. See \code{\link{createMergedResultsFile}} to create file.
#' @param shinyConfigPath  Path to shiny yml configuration file (use instead of sqliteDbPath or connectionDetails object)
#' @param runOverNetwork   (optional) Do you want the app to run over your network?
#' @param port             (optional) Only used if \code{runOverNetwork} = TRUE.
#' @param launch.browser   Should the app be launched in your default browser, or in a Shiny window.
#'                         Note: copying to clipboard will not work in a Shiny window.
#' @param enableAnnotation Enable annotation functionality in shiny app
#' @param aboutText        Text (using HTML markup) that will be displayed in an About tab in the Shiny app.
#'                         If not provided, no About tab will be shown.
#' @param tablePrefix      (Optional)  string to insert before table names (e.g. "cd_") for database table names
#' @param cohortTableName  (Optional) if cohort table name differs from the standard - cohort (ignores prefix if set)
#' @param databaseTableName (Optional) if database table name differs from the standard - database (ignores prefix if set)
#'
#' @param makePublishable (Optional) copy data files to make app publishable to posit connect/shinyapp.io
#' @param publishDir      If make publishable is true - the directory that the shiny app is copied to
#' @param overwritePublishDir      (Optional) If make publishable is true - overwrite the directory for publishing
    """
    if not vocabulary_database_schemas:
        vocabulary_database_schemas = results_database_schema

    if not publish_dir: 
        publish_dir = os.path.join(os.getcwd(), 'diagnostics_explorer')

    # filter non args
    args = {
        "sqliteDbPath": sqlite_db_path,
        "connectionDetails": connection_details,
        "shinyConfigPath": shiny_config_path,
        "resultsDatabaseSchema": results_database_schema,
        "vocabularyDatabaseSchema": vocabulary_database_schema,
        "vocabularyDatabaseSchemas": vocabulary_database_schemas,
        "tablePrefix": table_prefix,
        "cohortTableName": cohort_table_name,
        "databaseTableName": database_table_name,
        "aboutText": about_text,
        "runOverNetwork": run_over_network,
        "port": port,
        "makePublishable": make_publishable,
        "publishDir": publish_dir,
        "overwritePublishDir": overwrite_publish_dir,
        'launch.browser': launch_browser,
        "enableAnnotation": enable_annotation
    }    
    # remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return cohort_diagnostics.launchDiagnosticsExplorer(**args)