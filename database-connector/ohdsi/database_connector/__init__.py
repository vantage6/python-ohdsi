import os

from importlib.resources import files

from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import ListVector
from rpy2.robjects.methods import RS4

# When building documentation for the project, the following import will fail
# as the package is not installed. In this case, we set the variable to None
# so that the documentation can be built.
if os.environ.get('IGNORE_R_IMPORTS', False):
    database_connector_r = None
else:
    database_connector_r = importr('DatabaseConnector')


# -----------------------------------------------------------------------------
# wrapper: DatabaseConnector/R/Connect.R
# functions:
#    - createConnectionDetails (create_connection_details)
#    - connect (connect)
#    - disconnect (disconnect)
# -----------------------------------------------------------------------------
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

    - ``create_connection_details(dbms, user, password, server, port, \
                                    extraSettings, oracleDriver, \
                                    pathToDriver)``
    - ``create_connection_details(dbms, connectionString, pathToDriver)``
    - ``create_connection_details(dbms, connectionString, user, password, \
                                    pathToDriver)``

    Wraps the R ``DatabaseConnector::createConnectionDetails`` function defined
    in ``DatabaseConnector/R/Connect.R``.

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
    >>> create_connection_details(
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


def connect(connection_details: ListVector | None = None,
            dbms: str | None = None,
            user: str | None = None,
            password: str | None = None,
            server: str | None = None,
            port: int | None = None,
            extra_settings: str | None = None,
            oracle_driver: str = "thin",
            connection_string: str | None = None,
            path_to_driver: str | None = None) -> RS4:
    """
    Connect to a OMOP CDM database

    Connects to a database using the provided connection details, created by
    ``create_connection_details`` or from the arguments provided.

    Wraps the R ``DatabaseConnector::connect`` function defined in
    ``DatabaseConnector/R/Connect.R``.

    Parameters
    ----------
    connection_details : ListVector
        The connection details.
    dbms : str | None, optional
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
    RS4
        The database connection.

    Examples
    --------
    >>> connect(connection_details)
    """
    # The jar required is shipped with the package
    if not path_to_driver:
        jar = files('ohdsi.database_connector.java')
        # Hack to get the path to the folder of driver jar file,
        # as the files method returns a MultiPlexPath object which
        # does not allow simple conversion to string.
        path_to_driver = str(jar.joinpath(''))

    input_args = {
        "connectionDetails": connection_details,
        "dbms": dbms, "user": user, "password": password,
        "server": server, "port": port, "extraSettings": extra_settings,
        "oracleDriver": oracle_driver,
        "connectionString": connection_string,
        "pathToDriver": path_to_driver
    }
    # Remove None values
    input_args = {k: v for k, v in input_args.items() if v is not None}

    return database_connector_r.connect(**input_args)


def disconnect(connection: RS4) -> None:
    """
    Disconnect from a database

    Wraps the R ``DatabaseConnector::disconnect`` function defined in
    ``DatabaseConnector/R/Connect.R``.

    Parameters
    ----------
    connection : RS4
        The database connection.

    Examples
    --------
    >>> disconnect(connection)
    """
    database_connector_r.disconnect(connection)


# -----------------------------------------------------------------------------
# wrapper: DatabaseConnector/R/Sql.R
# functions:
#    - querySql (query_sql)
#    - executeSql (execute_sql)
# -----------------------------------------------------------------------------
def query_sql(connection: RS4, sql: str) -> RS4:
    """
    Query a database

    Wraps the R ``DatabaseConnector::querySql`` function defined in
    ``DatabaseConnector/R/Sql.R``.

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
    >>> query_sql(connection, sql)
    >>> query_sql(connection, "SELECT COUNT(*) FROM person")
    """
    return database_connector_r.querySql(connection, sql)


def execute_sql(connection: RS4, sql: str) -> None:
    """
    Execute a SQL statement

    Wraps the R ``DatabaseConnector::executeSql`` function defined in
    ``DatabaseConnector/R/Sql.R``.

    Parameters
    ----------
    connection : RS4
        The database connection.
    sql : str
        The SQL statement.

    Examples
    --------
    >>> execute_sql(connection, sql)
    >>> execute_sql(connection, "DROP TABLE IF EXISTS person")
    >>> execute_sql(
    ...     conn, "CREATE TABLE x (k INT); CREATE TABLE y (k INT);"
    ... )
    """
    database_connector_r.executeSql(connection, sql)
