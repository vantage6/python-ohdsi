from importlib.resources import files

from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import ListVector
from rpy2.robjects.methods import RS4


database_connector_r = importr('DatabaseConnector')


class Connect:

    @staticmethod
    def create_connection_details(
        dbms: str, user: str | None = None, password: str | None = None,
        server: str | None = None, port: int | None = None,
        extra_settings: str | None = None, oracle_driver: str = "thin",
        connection_string: str | None = None,
        path_to_driver: str | None = None
    ) -> ListVector:
        """
        Create Connection Details.

        Creates a list containing all details needed to connect to a database.
        There are three ways to call this function:

        - ``create_connection_details(dbms, user, password, server, port,
                                      extraSettings, oracleDriver,
                                      pathToDriver)``
        - ``create_connection_details(dbms, connectionString, pathToDriver)``
        - ``create_connection_details(dbms, connectionString, user, password,
                                      pathToDriver)``

        Parameters
        ----------
        dbms : str
            The DBMS type.
        user : str | None, optional
            The database user name. Required if ``connection_string`` is not
            provided.
        password : str | None, optional
            The database password. Required if ``connection_string`` is not
            provided.
        server : str | None, optional
            The database server name. Required if ``connection_string`` is not
            provided.
        port : int | None, optional
            The database server port. Required if ``connection_string`` is not
            provided.
        extra_settings : str | None, optional
            Additional database connection settings.
        oracle_driver : str, optional
            The Oracle driver to use. Defaults to ``thin``.
        connection_string : str | None, optional
            The database connection string. ``user``, ``password``, ``server``,
            and ``port`` are ignored if this is provided.
        path_to_driver : str | None, optional
            The path to the database driver jar file.

        Returns
        -------
        ListVector
            The connection details.

        Examples
        --------
        >>> Connect.create_connection_details(
        ...     dbms="postgresql", user="user", password="password",
        ...     server="localhost/postgres", port=5432
        ... )
        """
        # The jar required is shipped with the package
        if not path_to_driver:
            jar = files('ohdsi.database_connector.java')
            # Hack to get the path to the folder of driver jar file,
            # as the files method returns a MultiPlexPath object which
            # does not allow simple conversion to string.
            path_to_driver = str(jar.joinpath(''))

        input_args = {
            "dbms": dbms, "user": user, "password": password,
            "server": server, "port": port, "extraSettings": extra_settings,
            "oracleDriver": oracle_driver,
            "connectionString": connection_string,
            "pathToDriver": path_to_driver
        }
        # Remove None values
        input_args = {k: v for k, v in input_args.items() if v is not None}
        return database_connector_r.createConnectionDetails(**input_args)

    @staticmethod
    def connect(connection_details: ListVector) -> RS4:
        """
        Connect to a OMOP CDM database.

        Connects to a database using the provided connection details,
        created by ``create_connection_details``.

        Parameters
        ----------
        connection_details : ListVector
            The connection details.

        Returns
        -------
        RS4
            The database connection.

        Examples
        --------
        >>> Connect.connect(connection_details)
        """
        return database_connector_r.connect(connection_details)

    @staticmethod
    def disconnect(connection: RS4) -> None:
        """
        Disconnect from a database.

        Parameters
        ----------
        connection : RS4
            The database connection.

        Examples
        --------
        >>> Connect.disconnect(connection)
        """
        database_connector_r.disconnect(connection)


class Sql:

    @staticmethod
    def query_sql(connection: RS4, sql: str) -> RS4:
        """
        Query a database.

        Parameters
        ----------
        connection : RS4
            The database connection.
        sql : str
            The SQL query.

        Returns
        -------
        RS4
            The query result.

        Examples
        --------
        >>> Sql.query_sql(connection, sql)
        >>> Sql.query_sql(connection, "SELECT COUNT(*) FROM person")
        """
        return database_connector_r.querySql(connection, sql)

    @staticmethod
    def execute_sql(connection: RS4, sql: str) -> None:
        """
        Execute a SQL statement.

        Parameters
        ----------
        connection : RS4
            The database connection.
        sql : str
            The SQL statement.

        Examples
        --------
        >>> Sql.execute_sql(connection, sql)
        >>> Sql.execute_sql(connection, "DROP TABLE IF EXISTS person")
        >>> Sql.execute_sql(
        ...     conn, "CREATE TABLE x (k INT); CREATE TABLE y (k INT);"
        ... )
        """
        database_connector_r.executeSql(connection, sql)
