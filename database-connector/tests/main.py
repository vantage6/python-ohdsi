from ohdsi.database_connector import Connect, Sql

connection_details = Connect.create_connection_details(
    "postgresql",
    server="host.docker.internal/postgres",
    user="postgres",
    password="matchstick-wrapper-sliding-bulb",
    port=5432
)
con = Connect.connect(connection_details)

print(con)

result = Sql.query_sql(con, "SELECT * FROM omopcdm.person LIMIT 3")
print(result)

Sql.execute_sql(
    con,
    "CREATE TABLE foo (bar INT);"
)

Connect.disconnect(con)

print('Done')
