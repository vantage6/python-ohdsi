from ohdsi.feature_extraction import (
    DefaultCovariateSettings,
    DetailedCovariateSettings
)


covars = DefaultCovariateSettings.create_covariate_settings(
    use_demographics_gender=True,
    use_demographics_age_group=True,
    use_condition_occurrence_any_time_prior=True
)

default_covars = DetailedCovariateSettings.create_default_covariate_settings()
