from ohdsi.feature_extraction import (
    DefaultCovariateSettings,
    DetailedCovariateSettings,
    GetCovariates
)


covars = DefaultCovariateSettings.create_covariate_settings(
    use_demographics_gender=True,
    use_demographics_age_group=True,
    use_condition_occurrence_any_time_prior=True
)

default_covars = DetailedCovariateSettings.create_default_covariate_settings()

detailed_covars = DetailedCovariateSettings.\
    convert_prespec_settings_to_detailed_settings(default_covars)


from ohdsi.database_connector import (
    Connect
)

connection_details = Connect.create_connection_details(
    "postgresql",
    server="localhost/postgres",
    user="postgres",
    password="matchstick-wrapper-sliding-bulb",
    port=5432
)
con = Connect.connect(connection_details)

data = GetCovariates.get_db_covariate_data(
    cdm_database_schema="omopcdm",
    connection=con,
    cohort_database_schema="results",
    cohort_table="cohort",
    covariate_settings=default_covars,
)