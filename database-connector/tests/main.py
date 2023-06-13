from ohdsi.database_connector import Connect

connection_details = Connect.create_connection_details(
    "postgresql",
    server="localhost/postgres",
    user="postgres",
    password="matchstick-wrapper-sliding-bulb",
    port=5432
)
con = Connect.connect(connection_details)

print(con)

Connect.disconnect(con)

print('Done')