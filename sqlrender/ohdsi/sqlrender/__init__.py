import os

from pathlib import Path

from rpy2.robjects.vectors import StrVector
from rpy2.robjects.packages import importr
from rpy2.robjects.pandas2ri import rpy2py_dataframe
from pandas import DataFrame

#
# converters
#
# @robjects.default_converter.py2rpy.register(type(none))
# def _py_none_to_null(py_obj):
#     return robjects.null


#
# r interface
#
# When building documentation for the project, the following import will fail
# as the package is not installed. In this case, we set the variable to None
# so that the documentation can be built.
if os.environ.get('IGNORE_R_IMPORTS', False):
    base_r = None
    sql_render_r = None
else:
    base_r = importr('base')
    sql_render_r = importr('SqlRender')


# -----------------------------------------------------------------------------
# wrapper: SqlRender/R/SparkSql.R
# functions:
#    - sparkHandleInsert (spark_handle_insert)
# -----------------------------------------------------------------------------
def spark_handle_insert(sql, connection) -> StrVector:
    """
    Handles Spark Inserts

    This function is for Spark connections only, it handles insert
    commands, as Spark cannot handle inserts with aliased or subset
    columns.

    Wraps the R ``SqlRender::sparkHandleInsert`` function defined in
    ``SqlRender/R/SparkSql.R``.

    Parameters
    ----------
    sql : str
        The SQL to be translated.
    connection : str
        The connection to the database server.

    Returns
    -------
    StrVector
        A sql string with INSERT command modified to contain the full
        column list, padded with NULLS as needed.
    """
    return sql_render_r.sparkHandleInsert(sql, connection)


# -----------------------------------------------------------------------------
# wrapper: SqlRender/R/RenderSql.R
# functions:
#    - render (render)
#    - translate (translate)
#    - translateSingleStatement (translate_single_statement)
#    - splitSql (split_sql)
#    - getTempTablePrefix (get_temp_table_prefix)
# -----------------------------------------------------------------------------
def render(sql: str, warn_on_missing_parameters: bool = True, **kwargs) \
        -> StrVector:
    """
    Renders SQL code based on parameterized SQL and parameter values

    This function takes parameterized SQL and a list of parameter values
    and renders the SQL that can be send to the server.

    Wraps the R ``SqlRender::render`` function defined in
    ``SqlRender/R/RenderSql.R``.

    Parameters
    ----------
    sql : str
            The parameterized SQL.
    warnOnMissingParameters : bool
        Should a warning be raised when parameters provided to this
        function do not appear in the parameterized SQL that is being
        rendered? By default, this is True
    kwargs : dict
        The parameter values.

        Parameters
        ----------
        sql : str
             The parameterized SQL.
        warn_on_missing_parameters : bool
            Should a warning be raised when parameters provided to this
            function do not appear in the parameterized SQL that is being
            rendered? By default, this is True
        kwargs : dict
            The parameter values.

    Examples
    --------
    >>> sql = "SELECT * FROM table WHERE id = @id"
    >>> render("SELECT * FROM @a;", a = "myTable")
    """
    return sql_render_r.render(sql, warn_on_missing_parameters, **kwargs)


def translate(sql: str, target_dialect: str,
              temp_emulation_schema: str | None = None) -> StrVector:
    """
    Translates SQL from one dialect to another

    Wraps the R ``SqlRender::translate`` function defined in
    ``SqlRender/R/RenderSql.R``.

    Parameters
    ----------
    sql : str
        The SQL to be translated
    target_dialect : str
        The target dialect. Currently "oracle", "postgresql", "pdw",
        "impala", "sqlite", "sqlite extended", "netezza", "bigquery",
        "snowflake", "synapse", "spark", and "redshift" are supported.
        Use ``list_supported_dialects`` to get the list of supported
        dialects.
    temp_emulation_schema : str | None
        Some database platforms like Oracle and Impala do not truly support
        temp tables. To emulate temp tables, provide a schema with write
        privileges where temp tables can be created.

    Returns
    -------
    StrVector
        The translated SQL.
    """
    if not temp_emulation_schema:
        temp_emulation_schema = \
            base_r.getOption("sqlRenderTempEmulationSchema")

    return sql_render_r.translate(sql, target_dialect,
                                  temp_emulation_schema)


def translate_single_statement(
    sql: str, target_dialect: str, temp_emulation_schema: str | None = None
) -> StrVector:
    """
    Translates a single SQL statement from one dialect to another

    This function takes SQL in one dialect and translates it into another.
    It uses simple pattern replacement, so its functionality is limited.
    This removes any trailing semicolon as required by Oracle when
    sending through JDBC. An error is thrown if more than one statement
    is encountered in the SQL.

    Wraps the R ``SqlRender::translateSingleStatement`` function defined in
    ``SqlRender/R/RenderSql.R``.

    Parameters
    ----------
    sql : str
        The SQL to be translated
    target_dialect : str
        The target dialect. Currently "oracle", "postgresql", "pdw",
        "impala", "sqlite", "sqlite extended", "netezza", "bigquery",
        "snowflake", "synapse", "spark", and "redshift" are supported.
        Use ``list_supported_dialects`` to get the list of supported
        dialects.
    temp_emulation_schema : str | None
        Some database platforms like Oracle and Impala do not truly support
        temp tables. To emulate temp tables, provide a schema with write
        privileges where temp tables can be created.

    Returns
    -------
    str
        The translated SQL.

    Examples
    --------
    >>> translate_single_statement(
    >>>     "USE my_schema;",
    >>>     targetDialect = "oracle"
    >>> )
    """
    if not temp_emulation_schema:
        temp_emulation_schema = \
            base_r.getOption("sqlRenderTempEmulationSchema")

    return sql_render_r.translateSingleStatement(sql, target_dialect,
                                                 temp_emulation_schema)


def split_sql(sql: str) -> StrVector:
    """
    Split a single SQL string into one or more SQL statements

    ``splitSql`` splits a string containing multiple SQL statements into
    a vector of SQL statements. This function is needed because some DBMSs
    (like ORACLE) do not accepts multiple SQL statements being sent as one
    execution.

    Wraps the R ``SqlRender::splitSql`` function defined in
    ``SqlRender/R/RenderSql.R``.

    Parameters
    ----------
    sql : str
        The SQL string to split into separate statements

    Returns
    -------
    str
        A vector of strings, one for each SQL statement

    Examples
    --------
    >>> split_sql("SELECT * INTO a FROM b; USE x; DROP TABLE c;")
    """
    return sql_render_r.splitSql(sql)


def get_temp_table_prefix() -> StrVector:
    """
    Get the temporary table prefix

    Used for emulated temp tables for DBMSs that do not support temp tables
    (e.g. Oracle, BigQuery).

    Wraps the R ``SqlRender::getTempTablePrefix`` function defined in
    ``SqlRender/R/RenderSql.R``.

    Returns
    -------
    str
        The prefix used for emulated temp tables

    Examples
    --------
    >>> RenderSql.get_temp_table_prefix()
    """
    return sql_render_r.getTempTablePrefix()


# -----------------------------------------------------------------------------
# wrapper: SqlRender/R/HelperFunctions.R
# functions:
#    - readSql (read_sql)
#    - writeSql (write_sql)
#    - renderSqlFile (render_sql_file)
#    - translateSqlFile (translate_sql_file)
#    - loadRenderTranslateSql (load_render_translate_sql)
#    - listSupportedDialects (list_supported_dialects)
# -----------------------------------------------------------------------------
def read_sql(source_file: str | Path) -> StrVector:
    """
    loads SQL from a file

    Wraps the R ``SqlRender::readSql`` function defined in
    ``SqlRender/R/HelperFunctions.R``.

    Parameters
    ----------
    source_file : str | Path
        The source SQL file

    Returns
    -------
    StrVector
        The SQL from the file
    """
    return sql_render_r.readSql(source_file)


def write_sql(sql: str, file: str | Path) -> None:
    """
    Write SQL to a SQL (text) file

    Wraps the R ``SqlRender::writeSql`` function defined in
    ``SqlRender/R/HelperFunctions.R``.

    Parameters
    ----------
    sql : str
        The SQL to write
    file : str | Path
        The target SQL file

    Examples
    --------
    >>> write_sql("SELECT * FROM table;", "my_sql.sql")
    """
    sql_render_r.writeSql(sql, str(file))


def render_sql_file(
    source_file: str | Path, target_file: str | Path,
    warnOnMissingParameters: bool = True, **kwargs
) -> None:
    """
    Render a SQL file

    Renders SQL code in a file based on parameterized SQL and parameter values,
    and writes it to another file.

    Wraps the R ``SqlRender::renderSqlFile`` function defined in
    ``SqlRender/R/HelperFunctions.R``.

    Parameters
    ----------
    source_file : str | Path
        The source SQL file
    target_file : str | Path
        The target SQL file
    warnOnMissingParameters : bool, optional
        If ``True``, a warning is issued if a parameter is not found in
        the parameter list, by default ``True``
    kwargs
        The parameters to use for rendering

    Examples
    --------
    >>> renderSqlFile(
    >>>     "myParamStatement.sql",
    >>>     "myRenderedStatement.sql",
    >>>     a = "myTable"
    >>> )
    """
    sql_render_r.renderSqlFile(source_file, target_file,
                               warnOnMissingParameters, **kwargs)


def translate_sql_file(source_file: str | Path, target_file: str | Path,
                       target_dialect: str,
                       temp_emulation_schema: str | None = None) -> None:
    """
    Translate a SQL file

    This function takes SQL and translates it to a different dialect.

    Wraps the R ``SqlRender::translateSqlFile`` function defined in
    ``SqlRender/R/HelperFunctions.R``.

    Parameters
    ----------
    source_file : str | Path
        The source SQL file
    target_file : str | Path
        The target SQL file
    target_dialect : str
        The target dialect. Currently "oracle", "postgresql", "pdw",
        "impala", "sqlite", "sqlite extended", "netezza", "bigquery",
        "snowflake", "synapse", "spark", and "redshift" are supported.
        Use ``list_supported_dialects`` to get the list of supported
        dialects.
    temp_emulation_schema : str | None
        Some database platforms like Oracle and Impala do not truly support
        temp tables. To emulate temp tables, provide a schema with write
        privileges where temp tables can be created.

    Examples
    --------
    >>> translateSqlFile(
    >>>     "mySql.sql",
    >>>     "myTranslatedSql.sql",
    >>>     targetDialect = "oracle"
    >>> )
    """
    if not temp_emulation_schema:
        temp_emulation_schema = \
            base_r.getOption("sqlRenderTempEmulationSchema")

    sql_render_r.translateSqlFile(source_file, target_file, target_dialect,
                                  temp_emulation_schema)


def load_render_translate_sql(
    sql_file: str | Path, package_name: str, dbms: str,
    temp_emulation_schema: str | None = None,
    warn_on_missing_parameters: bool = True
) -> StrVector:
    """
    Load, render, and translate a SQL file in a package

    ``loadRenderTranslateSql`` Loads a SQL file contained in a package,
    renders it and translates it to the specified dialect.

    Wraps the R ``SqlRender::loadRenderTranslateSql`` function defined in
    ``SqlRender/R/HelperFunctions.R``.

    Parameters
    ----------
    sql_file : str | Path
        The source SQL file
    package_name : str
        The package name
    dbms : str
        The target dialect. Currently "oracle", "postgresql", "pdw",
        "impala", "sqlite", "sqlite extended", "netezza", "bigquery",
        "snowflake", "synapse", "spark", and "redshift" are supported.
        Use ``list_supported_dialects`` to get the list of supported
        dialects.
    temp_emulation_schema : str | None
        Some database platforms like Oracle and Impala do not truly support
        temp tables. To emulate temp tables, provide a schema with write
        privileges where temp tables can be created.
    warn_on_missing_parameters : bool, optional
        If ``True``, a warning is issued if a parameter is not found in
        the parameter list, by default ``True``
    """
    if not temp_emulation_schema:
        temp_emulation_schema = \
            base_r.getOption("sqlRenderTempEmulationSchema")

    return sql_render_r.loadRenderTranslateSql(
        sql_file, package_name, dbms, temp_emulation_schema,
        warnOnMissingParameters=warn_on_missing_parameters
    )


def list_supported_dialects() -> DataFrame:
    """
    List the supported dialects

    Wraps the R ``SqlRender::listSupportedDialects`` function defined in
    ``SqlRender/R/HelperFunctions.R``.

    Returns
    -------
    DataFrame
        A dataframe with the supported dialects
    """
    return rpy2py_dataframe(sql_render_r.listSupportedDialects())
