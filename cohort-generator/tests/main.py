from ohdsi.cohort_generator import CohortTables
from ohdsi.database_connector import Connect

table_names = CohortTables.get_cohort_table_names()

con_details = Connect.create_connection_details(
    "postgresql",
    server="localhost/postgres",
    user="postgres",
    password="matchstick-wrapper-sliding-bulb",
    port=5432
)

con = Connect.connect(
    connection_details=con_details
)

res = CohortTables.create_cohort_tables(
    connection=con,
    cohort_database_schema="results",
    cohort_table_names=table_names
)
