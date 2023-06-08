from pathlib import Path
from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import StrVector

from rpy2.robjects.packages import importr

#
# converters
#
# @robjects.default_converter.py2rpy.register(type(none))
# def _py_none_to_null(py_obj):
#     return robjects.null


#
# r interface
#
sql_render_r = importr('SqlRender')
base_r = importr('base')


#
# python wrappers
#
class SparkSql:

    @staticmethod
    def spark_handle_insert(sql, connection) -> StrVector:
        """
        Handles Spark Inserts

        This function is for Spark connections only, it handles insert
        commands, as Spark cannot handle inserts with aliased or subset
        columns.

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


class RenderSql:

    @staticmethod
    def render(sql: str, warn_on_missing_parameters: bool = True, **kwargs) \
            -> StrVector:
        """
        Renders SQL code based on parameterized SQL and parameter values.

        This function takes parameterized SQL and a list of parameter values
        and renders the SQL that can be send to the server.

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

        Returns
        -------
        StrVector
            The rendered SQL.

        Examples
        --------
        >>> sql = "SELECT * FROM table WHERE id = @id"
        >>> RenderSql.render("SELECT * FROM @a;", a = "myTable")
        """
        return sql_render_r.render(sql, warn_on_missing_parameters, **kwargs)

    @staticmethod
    def translate(sql: str, target_dialect: str,
                  temp_emulation_schema: str | None) -> StrVector:
        """
        ``translate`` translates SQL from one dialect to another.

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

    @staticmethod
    def translate_single_statement(
        sql: str, target_dialect: str, temp_emulation_schema: str | None
    ) -> StrVector:
        """
        Translates a single SQL statement from one dialect to another.

        This function takes SQL in one dialect and translates it into another.
        It uses simple pattern replacement, so its functionality is limited.
        This removes any trailing semicolon as required by Oracle when
        sending through JDBC. An error is thrown if more than one statement
        is encountered in the SQL.

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
        >>> RenderSql.translate_single_statement(
        >>>     "USE my_schema;",
        >>>     targetDialect = "oracle"
        >>> )
        """
        if not temp_emulation_schema:
            temp_emulation_schema = \
                base_r.getOption("sqlRenderTempEmulationSchema")

        return sql_render_r.translateSingleStatement(sql, target_dialect,
                                                     temp_emulation_schema)

    @staticmethod
    def split_sql(sql: str) -> StrVector:
        """
        Split a single SQL string into one or more SQL statements

        ``splitSql`` splits a string containing multiple SQL statements into
        a vector of SQL statements. This function is needed because some DBMSs
        (like ORACLE) do not accepts multiple SQL statements being sent as one
        execution.

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
        >>> RenderSql.split_sql("SELECT * INTO a FROM b; USE x; DROP TABLE c;")
        """
        return sql_render_r.splitSql(sql)

    @staticmethod
    def get_temp_table_prefix() -> StrVector:
        """
        Get the prefix used for emulated temp tables for DBMSs that do not
        support temp tables (e.g. Oracle, BigQuery).

        Returns
        -------
        str
            The prefix used for emulated temp tables

        Examples
        --------
        >>> RenderSql.get_temp_table_prefix()
        """
        return sql_render_r.getTempTablePrefix()


class HelperFunctions:

    @staticmethod
    def read_sql(source_file: str | Path) -> StrVector:
        """
        loads SQL from a file

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

    @staticmethod
    def write_sql(sql: str, file: str | Path) -> None:
        """
        Write SQL to a SQL (text) file

        Parameters
        ----------
        sql : str
            The SQL to write
        file : str | Path
            The target SQL file

        Examples
        --------
        >>> RenderSql.write_sql("SELECT * FROM table;", "my_sql.sql")
        """
        sql_render_r.writeSql(sql, str(file))

    @staticmethod
    def render_sql_file(
        source_file: str | Path, target_file: str | Path,
        warnOnMissingParameters: bool = True, **kwargs
    ) -> None:
        """
        Render a SQL file

        ``renderSqlFile`` Renders SQL code in a file based on parameterized
        SQL and parameter values, and writes it to another file.

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
        >>> HelperFunctions.renderSqlFile(
        >>>     "myParamStatement.sql",
        >>>     "myRenderedStatement.sql",
        >>>     a = "myTable"
        >>> )
        """
        sql_render_r.renderSqlFile(source_file, target_file,
                                   warnOnMissingParameters, **kwargs)

    @staticmethod
    def translate_sql_file(source_file: str | Path, target_file: str | Path,
                           target_dialect: str,
                           temp_emulation_schema: str | None) -> None:
        """
        Translate a SQL file.

        This function takes SQL and translates it to a different dialect.

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
        >>> HelperFunctions.translateSqlFile(
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

    @staticmethod
    def load_render_translate_sql(sql_file: str | Path, package_name: str,
                                  dbms: str, temp_emulation_schema: str | None,
                                  warn_on_missing_parameters: bool = True) \
            -> StrVector:
        """
        Load, render, and translate a SQL file in a package.

        ``loadRenderTranslateSql`` Loads a SQL file contained in a package,
        renders it and translates it to the specified dialect'

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

        Examples



        """
        if not temp_emulation_schema:
            temp_emulation_schema = \
                base_r.getOption("sqlRenderTempEmulationSchema")

        return sql_render_r.loadRenderTranslateSql(
            sql_file, package_name, dbms, temp_emulation_schema,
            warnOnMissingParameters=warn_on_missing_parameters
        )

    @staticmethod
    def list_supported_dialects() -> RS4:
        """
        List the supported dialects.

        Returns
        -------
        RS4
            A R wrapped dataframe

        TODO : make this a pandas dataframe
        """
        return sql_render_r.listSupportedDialects()
