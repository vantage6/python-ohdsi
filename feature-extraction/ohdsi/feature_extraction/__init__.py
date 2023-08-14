import os
import json

from typing import Any

from rpy2 import robjects
from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import DataFrame, IntVector, ListVector
from rpy2.robjects.packages import importr

from ohdsi.common import (
    ListVectorExtended,
    CovariateData,
    convert_bool_from_r
)


if os.environ.get('IGNORE_R_IMPORTS', False):
    extractor_r = None
else:
    extractor_r = importr('FeatureExtraction')


#
# Converters
#
@robjects.default_converter.py2rpy.register(type(None))
def _py_none_to_null(py_obj):
    return robjects.NULL


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/Aggregation.R
# functions:
#    - aggregateCovariates (aggregate_covariates)
# -----------------------------------------------------------------------------
def aggregate_covariates(covariate_data: RS4) -> RS4:
    """
    Aggregate covariate data

    Wraps the R ``FeatureExtraction::aggregateCovariates`` function defined in
    ``FeatureExtraction/R/Aggregation.R``.

    Parameters
    ----------
    covariate_data : RS4
        An object of type ``covariateData`` as generated using
        ``getDbCovariateData``.

    Returns
    -------
    RS4
        An object of class ``covariateData``.

    Examples
    --------
    >>> covariate_data = create_empty_covariate_data(
    ...     cohort_id = 1,
    ...     aggregated = False,
    ...     temporal = False
    ... )
    ... aggregated_covariate_data = aggregate_covariates(covariate_data)
    """
    return CovariateData.from_RS4(
        extractor_r.aggregateCovariates(covariate_data)
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/CompareCohorts.R
# functions:
#    - computeStandardizedDifference (compute_standardized_difference)
# -----------------------------------------------------------------------------
def compute_standardized_difference(
        covariate_data1: RS4, covariate_data2: RS4,
        cohort_id1: int | None = None, cohort_id2: int | None = None
        ) -> DataFrame:
    """
    Compute standardized difference of mean for all covariates.

    Computes the standardized difference for all covariates between two
    cohorts. The standardized difference is defined as the difference
    between the mean divided by the overall standard deviation.

    Wraps the R ``FeatureExtraction::computeStandardizedDifference`` function
    defined in ``FeatureExtraction/R/CompareCohorts.R``.

    Parameters
    ----------
    covariate_data1 : RS4
        The covariate data of the first cohort. Needs to be in aggregated
        format.
    covariate_data2 : RS4
        The covariate data of the second cohort. Needs to be in aggregated
        format.
    cohort_id1 : int | None
        If provided, ``covariateData1`` will be restricted to this cohort.
        If not provided, ``covariateData1`` is assumed to contain data on
        only 1 cohort.
    cohort_id2: int | None
        If provided, ``covariateData2`` will be restricted to this cohort.
        If not provided, ``covariateData2`` is assumed to contain data on
        only 1 cohort.

    Returns
    -------
    DataFrame
        A data frame with means and standard deviations per cohort as well
        as the standardized difference of mean.

    Examples
    --------
    >>> cov_data_diff = compute_standardized_difference(
    ...     covariate_data1,
    ...     covariate_data2,
    ...     cohort_id1 = 1,
    ...     cohort_id2 = 2
    ... )
    """
    # TODO: check that the return type is correct
    return extractor_r.computeStandardizedDifference(
        covariate_data1, covariate_data2,
        cohort_id1, cohort_id2)


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/CovariateData.R
# functions:
#    - saveCovariateData (save_covariate_data)
#    - loadCovariateData (load_covariate_data)
#    - isCovariateData (is_covariate_data)
#    - isAggregatedCovariateData (is_aggregated_covariate_data)
#    - isTemporalCovariateData (is_temporal_covariate_data)
#    - createEmptyCovariateData (create_empty_covariate_data)
# -----------------------------------------------------------------------------
def save_covariate_data(covariate_data: RS4, file: str) -> None:
    """
    Save the covariate data to folder

    This function saves an object of type ``covariateData``. The data will
    be written to a file specified by the user.

    Wraps the R ``FeatureExtraction::saveCovariateData`` function defined in
    ``FeatureExtraction/R/CovariateData.R``.

    Parameters
    ----------
    covariate_data : RS4
        An object of type ``covariateData`` as generated using
        ``getDbCovariateData``.
    file : str
        The name of the file where the data will be written.

    Side Effects
    ------------
    A file containing an object of class ``covariateData`` will be written to
    the file system.

    Examples
    --------
    >>> save_covariate_data(covariate_data, file = filename)
    """
    return extractor_r.saveCovariateData(covariate_data, file)


def load_covariate_data(file: str, read_only: bool | None = False) \
        -> CovariateData:
    """
    Load the covariate data from a folder

    This function loads an object of type covariateData from a folder in
    the file system.

    Wraps the R ``FeatureExtraction::loadCovariateData`` function defined in
    ``FeatureExtraction/R/CovariateData.R``.

    Parameters
    ----------
    file : str
        The name of the file containing the data.
    read_only: bool | None
        DEPRECATED: If True, the data is opened read only.

    Returns
    -------
    CovariateData
        An object of class ``CovariateData``.

    Examples
    --------
    >>> covariate_data = load_covariate_data(filename)
    """
    return CovariateData.from_RS4(
        extractor_r.loadCovariateData(file, read_only)
    )


def is_covariate_data(x: Any) -> bool:
    """
    Check whether an object is a ``CovariateData`` object

    Wraps the R ``FeatureExtraction::isCovariateData`` function defined in
    ``FeatureExtraction/R/CovariateData.R``.

    Parameters
    ----------
    x : Any
        The object to check.

    Returns
    -------
    bool
        True if ``x`` is a ``CovariateData`` object, False otherwise.

    Examples
    --------
    >>> is_cov_data = is_covariate_data(covariate_data)
    """
    return convert_bool_from_r(extractor_r.isCovariateData(x))


def is_aggregated_covariate_data(x: Any) -> bool:
    """
    Check whether covariate data is aggregated

    Wraps the R ``FeatureExtraction::isAggregatedCovariateData`` function
    defined in ``FeatureExtraction/R/CovariateData.R``.

    Parameters
    ----------
    x : Any
        The covariate data object to check.

    Returns
    -------
    bool
        True if ``x`` is an aggregated ``CovariateData`` object, False
        otherwise.

    Examples
    --------
    >>> is_aggregated_cov_data = is_aggregated_covariate_data(covariate_data)
    """
    return convert_bool_from_r(extractor_r.isAggregatedCovariateData(x))


def is_temporal_covariate_data(x: Any) -> bool:
    """
    Check whether covariate data is temporal

    Wraps the R ``FeatureExtraction::isTemporalCovariateData`` function
    defined in ``FeatureExtraction/R/CovariateData.R``.

    Parameters
    ----------
    x : Any
        The covariate data object to check.

    Returns
    -------
    bool
        True if ``x`` is a temporal ``CovariateData`` object, False
        otherwise.

    Examples
    --------
    >>> is_temp_cov_data = is_temporal_covariate_data(covariate_data)
    """
    return convert_bool_from_r(extractor_r.isTemporalCovariateData(x))


def create_empty_covariate_data(cohort_id: int = 1, aggregated: bool = False,
                                temporal: bool = False) -> CovariateData:
    """
    Creates an empty covariate data object

    Wraps the R ``FeatureExtraction:::createEmptyCovariateData`` function
    defined in ``FeatureExtraction/R/CovariateData.R``.

    Parameters
    ----------
    cohort_id
        cohort number
    aggregated
        if the data should be aggregated
    temporal
        if the data is temporal

    Returns
    -------
    CovariateData
        An object of type ``CovariateData``.

    Examples
    --------
    >>> covariate_data = create_empty_covariate_data(
    ...     cohort_id = 1,
    ...     aggregated = False,
    ...     temporal = False
    ... )
    """
    return CovariateData.from_RS4(
        extractor_r.createEmptyCovariateData(cohort_id, aggregated, temporal)
    )

# TODO Implement the following:
# setMethod("show", "CovariateData", function(object)


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/DefaultCovariateSettings.R
# functions:
#    - createCovariateSettings (create_covariate_settings)
# -----------------------------------------------------------------------------
def create_covariate_settings(
    use_demographics_gender: bool = False,
    use_demographics_age: bool = False,
    use_demographics_age_group: bool = False,
    use_demographics_race: bool = False,
    use_demographics_ethnicity: bool = False,
    use_demographics_index_year: bool = False,
    use_demographics_index_month: bool = False,
    use_demographics_prior_observation_time: bool = False,
    use_demographics_post_observation_time: bool = False,
    use_demographics_time_in_cohort: bool = False,
    use_demographics_index_year_month: bool = False,
    use_care_site_id: bool = False,
    use_condition_occurrence_any_time_prior: bool = False,
    use_condition_occurrence_long_term: bool = False,
    use_condition_occurrence_medium_term: bool = False,
    use_condition_occurrence_short_term: bool = False,
    use_condition_occurrence_primary_inpatient_any_time_prior:
    bool = False,
    use_condition_occurrence_primary_inpatient_long_term: bool = False,
    use_condition_occurrence_primary_inpatient_medium_term: bool = False,
    use_condition_occurrence_primary_inpatient_short_term: bool = False,
    use_condition_era_any_time_prior: bool = False,
    use_condition_era_long_term: bool = False,
    use_condition_era_medium_term: bool = False,
    use_condition_era_short_term: bool = False,
    use_condition_era_overlapping: bool = False,
    use_condition_era_start_long_term: bool = False,
    use_condition_era_start_medium_term: bool = False,
    use_condition_era_start_short_term: bool = False,
    use_condition_group_era_any_time_prior: bool = False,
    use_condition_group_era_long_term: bool = False,
    use_condition_group_era_medium_term: bool = False,
    use_condition_group_era_short_term: bool = False,
    use_condition_group_era_overlapping: bool = False,
    use_condition_group_era_start_long_term: bool = False,
    use_condition_group_era_start_medium_term: bool = False,
    use_condition_group_era_start_short_term: bool = False,
    use_drug_exposure_any_time_prior: bool = False,
    use_drug_exposure_long_term: bool = False,
    use_drug_exposure_medium_term: bool = False,
    use_drug_exposure_short_term: bool = False,
    use_drug_era_any_time_prior: bool = False,
    use_drug_era_long_term: bool = False,
    use_drug_era_medium_term: bool = False,
    use_drug_era_short_term: bool = False,
    use_drug_era_overlapping: bool = False,
    use_drug_era_start_long_term: bool = False,
    use_drug_era_start_medium_term: bool = False,
    use_drug_era_start_short_term: bool = False,
    use_drug_group_era_any_time_prior: bool = False,
    use_drug_group_era_long_term: bool = False,
    use_drug_group_era_medium_term: bool = False,
    use_drug_group_era_short_term: bool = False,
    use_drug_group_era_overlapping: bool = False,
    use_drug_group_era_start_long_term: bool = False,
    use_drug_group_era_start_medium_term: bool = False,
    use_drug_group_era_start_short_term: bool = False,
    use_procedure_occurrence_any_time_prior: bool = False,
    use_procedure_occurrence_long_term: bool = False,
    use_procedure_occurrence_medium_term: bool = False,
    use_procedure_occurrence_short_term: bool = False,
    use_device_exposure_any_time_prior: bool = False,
    use_device_exposure_long_term: bool = False,
    use_device_exposure_medium_term: bool = False,
    use_device_exposure_short_term: bool = False,
    use_measurement_any_time_prior: bool = False,
    use_measurement_long_term: bool = False,
    use_measurement_medium_term: bool = False,
    use_measurement_short_term: bool = False,
    use_measurement_value_any_time_prior: bool = False,
    use_measurement_value_long_term: bool = False,
    use_measurement_value_medium_term: bool = False,
    use_measurement_value_short_term: bool = False,
    use_measurement_range_group_any_time_prior: bool = False,
    use_measurement_range_group_long_term: bool = False,
    use_measurement_range_group_medium_term: bool = False,
    use_measurement_range_group_short_term: bool = False,
    use_observation_any_time_prior: bool = False,
    use_observation_long_term: bool = False,
    use_observation_medium_term: bool = False,
    use_observation_short_term: bool = False,
    use_charlson_index: bool = False,
    use_dcsi: bool = False,
    use_chads2: bool = False,
    use_chads2_vasc: bool = False,
    use_hfrs: bool = False,
    use_distinct_condition_count_long_term: bool = False,
    use_distinct_condition_count_medium_term: bool = False,
    use_distinct_condition_count_short_term: bool = False,
    use_distinct_ingredient_count_long_term: bool = False,
    use_distinct_ingredient_count_medium_term: bool = False,
    use_distinct_ingredient_count_short_term: bool = False,
    use_distinct_procedure_count_long_term: bool = False,
    use_distinct_procedure_count_medium_term: bool = False,
    use_distinct_procedure_count_short_term: bool = False,
    use_distinct_measurement_count_long_term: bool = False,
    use_distinct_measurement_count_medium_term: bool = False,
    use_distinct_measurement_count_short_term: bool = False,
    use_distinct_observation_count_long_term: bool = False,
    use_distinct_observation_count_medium_term: bool = False,
    use_distinct_observation_count_short_term: bool = False,
    use_visit_count_long_term: bool = False,
    use_visit_count_medium_term: bool = False,
    use_visit_count_short_term: bool = False,
    use_visit_concept_count_long_term: bool = False,
    use_visit_concept_count_medium_term: bool = False,
    use_visit_concept_count_short_term: bool = False,
    long_term_start_days: int = -365,
    medium_term_start_days: int = -180,
    short_term_start_days: int = -30,
    end_days: int = 0,
    included_covariate_concept_ids: list = [],
    add_descendants_to_include: bool = False,
    excluded_covariate_concept_ids: list = [],
    add_descendants_to_exclude: bool = False,
    included_covariate_ids: list = []
) -> ListVectorExtended:
    """
    Create covariate settings

    Creates an object specifying how covariates should be constructed
    from data in the CDM model.

    Wraps the R ``FeatureExtraction::createCovariateSettings`` function
    defined in ``FeatureExtraction/R/DefaultCovariateSettings.R``.

    Parameters
    ----------
    use_demographics_gender: bool
        Gender of the subject. (analysis ID 1)
    use_demographics_age: bool
        Age of the subject in years at the index date. (analysis ID 2)
    use_demographics_age_group: bool
        Age group of the subject at the index date. (analysis ID 3)
    use_demographics_race
        Race of the subject. (analysis ID 4)
    use_demographics_ethnicity
        Ethnicity of the subject. (analysis ID 5)
    use_demographics_index_year
        Year of the index date. (analysis ID 6)
    use_demographics_index_month
        Month of the index date. (analysis ID 7)
    use_demographics_prior_observation_time
        Number of continuous days of observation time preceding the index
        date. (analysis ID 8)
    use_demographics_post_observation_time
        Number of continuous days of observation time following the index
        date. (analysis ID 9)
    use_demographics_time_in_cohort
        Number of days of observation time during cohort period. (analysis
        ID 10)
    use_demographics_index_year_month
        Both calendar year and month of the index date in a single
        variable. (analysis ID 11)
    use_care_site_id
        Care site associated with the cohort start, pulled from the
        visit_detail, visit_occurrence, or person table, in that order.
        (analysis ID 12)
    use_condition_occurrence_any_time_prior
        One covariate per condition in the condition_occurrence table
        starting any time prior to index. (analysis ID 101)
    use_condition_occurrence_long_term
        One covariate per condition in the condition_occurrence table
        starting in the long term window. (analysis ID 102)
    use_condition_occurrence_medium_term
        One covariate per condition in the condition_occurrence table
        starting in the medium term window. (analysis ID 103)
    use_condition_occurrence_short_term
        One covariate per condition in the condition_occurrence table
        starting in the short term window. (analysis ID 104)
    use_condition_occurrence_primary_inpatient_any_time_prior
        One covariate per condition observed as a primary diagnosis in an
        inpatient setting in the condition_occurrence table starting any
        time prior to index. (analysis ID 105)
    use_condition_occurrence_primary_inpatient_long_term
        One covariate per condition observed as a primary diagnosis in an
        inpatient setting in the condition_occurrence table starting in
        the long term window. (analysis ID 106)
    use_condition_occurrence_primary_inpatient_medium_term
        One covariate per condition observed as a primary diagnosis in an
        inpatient setting in the condition_occurrence table starting in
        the medium term window. (analysis ID 107)
    use_condition_occurrence_primary_inpatient_short_term
        One covariate per condition observed as a primary diagnosis in an
        inpatient setting in the condition_occurrence table starting in
        the short term window. (analysis ID 108)
    use_condition_era_any_time_prior
        One covariate per condition in the condition_era table overlapping
        with any time prior to index. (analysis ID 201)
    use_condition_era_long_term
        One covariate per condition in the condition_era table overlapping
        with any part of the long term window. (analysis ID 202)
    use_condition_era_medium_term
        One covariate per condition in the condition_era table overlapping
        with any part of the medium term window. (analysis ID 203)
    use_condition_era_short_term
        One covariate per condition in the condition_era table overlapping
        with any part of the short term window. (analysis ID 204)
    use_condition_era_overlapping
        One covariate per condition in the condition_era table overlapping
        with the end of the risk window. (analysis ID 205)
    use_condition_era_start_long_term
        One covariate per condition in the condition_era table starting in
        the long term window. (analysis ID 206)
    use_condition_era_start_medium_term
        One covariate per condition in the condition_era table starting in
        the medium term window. (analysis ID 207)
    use_condition_era_start_short_term
        One covariate per condition in the condition_era table starting in
        the short term window. (analysis ID 208)
    use_condition_group_era_any_time_prior
        One covariate per condition era rolled up to groups in the
        condition_era table overlapping with any time prior to index.
        (analysis ID 209)
    use_condition_group_era_long_term
        One covariate per condition era rolled up to groups in the
        condition_era table overlapping with any part of the long term
        window. (analysis ID 210)
    use_condition_group_era_medium_term
        One covariate per condition era rolled up to groups in the
        condition_era table overlapping with any part of the medium term
        window. (analysis ID 211)
    use_condition_group_era_short_term
        One covariate per condition era rolled up to groups in the
        condition_era table overlapping with any part of the short term
        window. (analysis ID 212)
    use_condition_group_era_overlapping
        One covariate per condition era rolled up to groups in the
        condition_era table overlapping with the end of the risk window.
        (analysis ID 213)
    use_condition_group_era_start_long_term
        One covariate per condition era rolled up to groups in the
        condition_era table starting in the long term window. (analysis ID
        214)
    use_condition_group_era_start_medium_term
        One covariate per condition era rolled up to groups in the
        condition_era table starting in the medium term window. (analysis
        ID 215)
    use_condition_group_era_start_short_term
        One covariate per condition era rolled up to groups in the
        condition_era table starting in the short term window. (analysis
        ID 216)
    use_drug_exposure_any_time_prior
        One covariate per drug in the drug_exposure table starting any
        time prior to index. (analysis ID 301)
    use_drug_exposure_long_term
        One covariate per drug in the drug_exposure table starting in the
        long term window. (analysis ID 302)
    use_drug_exposure_medium_term
        One covariate per drug in the drug_exposure table starting in the
        medium term window. (analysis ID 303)
    use_drug_exposure_short_term
        One covariate per drug in the drug_exposure table starting in the
        short term window. (analysis ID 304)
    use_drug_era_any_time_prior
        One covariate per drug in the drug_era table overlapping with any
        time prior to index. (analysis ID 401)
    use_drug_era_long_term
        One covariate per drug in the drug_era table overlapping with any
        part of the long term window. (analysis ID 402)
    use_drug_era_medium_term
        One covariate per drug in the drug_era table overlapping with any
        part of the medium term window. (analysis ID 403)
    use_drug_era_short_term
        One covariate per drug in the drug_era table overlapping with any
        part of the short window. (analysis ID 404)
    use_drug_era_overlapping
        One covariate per drug in the drug_era table overlapping with the
        end of the risk window. (analysis ID 405)
    use_drug_era_start_long_term
        One covariate per drug in the drug_era table starting in the long
        term window. (analysis ID 406)
    use_drug_era_start_medium_term
        One covariate per drug in the drug_era table starting in the
        medium term window. (analysis ID 407)
    use_drug_era_start_short_term
        One covariate per drug in the drug_era table starting in the long
        short window. (analysis ID 408)
    use_drug_group_era_any_time_prior
        One covariate per drug rolled up to ATC groups in the drug_era
        table overlapping with any time prior to index. (analysis ID 409)
    use_drug_group_era_long_term
        One covariate per drug rolled up to ATC groups in the drug_era
        table overlapping with any part of the long term window.
        (analysis ID 410)
    use_drug_group_era_medium_term
        One covariate per drug rolled up to ATC groups in the drug_era
        table overlapping with any part of the medium term window.
        (analysis ID 411)
    use_drug_group_era_short_term
        One covariate per drug rolled up to ATC groups in the drug_era
        table overlapping with any part of the short term window.
        (analysis ID 412)
    use_drug_group_era_overlapping
        One covariate per drug rolled up to ATC groups in the drug_era
        table overlapping with the end of the risk window. (analysis ID
        413)
    use_drug_group_era_start_long_term
        One covariate per drug rolled up to ATC groups in the drug_era
        table starting in the long term window. (analysis ID 414)
    use_drug_group_era_start_medium_term
        One covariate per drug rolled up to ATC groups in the drug_era
        table starting in the medium term window. (analysis ID 415)
    use_drug_group_era_start_short_term
        One covariate per drug rolled up to ATC groups in the drug_era
        table starting in the short term window. (analysis ID 416)
    use_procedure_occurrence_any_time_prior
        One covariate per procedure in the procedure_occurrence table any
        time prior to index. (analysis ID 501)
    use_procedure_occurrence_long_term
        One covariate per procedure in the procedure_occurrence table in
        the long term window. (analysis ID 502)
    use_procedure_occurrence_medium_term
        One covariate per procedure in the procedure_occurrence table in
        the medium term window. (analysis ID 503)
    use_procedure_occurrence_short_term
        One covariate per procedure in the procedure_occurrence table in
        the short term window. (analysis ID 504)
    use_device_exposure_any_time_prior
        One covariate per device in the device exposure table starting any
        time prior to index. (analysis ID 601)
    use_device_exposure_long_term
        One covariate per device in the device exposure table starting in
        the long term window. (analysis ID 602)
    use_device_exposure_medium_term
        One covariate per device in the device exposure table starting in
        the medium term window. (analysis ID 603)
    use_device_exposure_short_term
        One covariate per device in the device exposure table starting in
        the short term window. (analysis ID 604)
    use_measurement_any_time_prior
        One covariate per measurement in the measurement table any time
        prior to index. (analysis ID 701)
    use_measurement_long_term
        One covariate per measurement in the measurement table in the long
        term window. (analysis ID 702)
    use_measurement_medium_term
        One covariate per measurement in the measurement table in the
        medium term window. (analysis ID 703)
    use_measurement_short_term
        One covariate per measurement in the measurement table in the
        short term window. (analysis ID 704)
    use_measurement_value_any_time_prior
        One covariate containing the value per measurement-unit
        combination any time prior to index. (analysis ID 705)
    use_measurement_value_long_term
        One covariate containing the value per measurement-unit
        combination in the long term window. (analysis ID 706)
    use_measurement_value_medium_term
        One covariate containing the value per measurement-unit
        combination in the medium term window. (analysis ID 707)
    use_measurement_value_short_term
        One covariate containing the value per measurement-unit
        combination in the short term window. (analysis ID 708)
    use_measurement_range_group_any_time_prior
        Covariates indicating whether measurements are below, within, or
        above normal range any time prior to index. (analysis ID 709)
    use_measurement_range_group_long_term
        Covariates indicating whether measurements are below, within, or
        above normal range in the long term window. (analysis ID 710)
    use_measurement_range_group_medium_term
        Covariates indicating whether measurements are below, within, or
        above normal range in the medium term window. (analysis ID 711)
    use_measurement_range_group_short_term
        Covariates indicating whether measurements are below, within, or
        above normal range in the short term window. (analysis ID 712)
    use_observation_any_time_prior
        One covariate per observation in the observation table any time
        prior to index. (analysis ID 801)
    use_observation_long_term
        One covariate per observation in the observation table in the long
        term window. (analysis ID 802)
    use_observation_medium_term
        One covariate per observation in the observation table in the
        medium term window. (analysis ID 803)
    use_observation_short_term
        One covariate per observation in the observation table in the
        short term window. (analysis ID 804)
    use_charlson_index
        The Charlson comorbidity index (Romano adaptation) using all
        conditions prior to the window end. (analysis ID 901)
    use_dcsi
        The Diabetes Comorbidity Severity Index (DCSI) using all
        conditions prior to the window end. (analysis ID 902)
    use_chads2
        The CHADS2 score using all conditions prior to the window end.
        (analysis ID 903)
    use_chads2_vasc
        The CHADS2VASc score using all conditions prior to the window end.
        (analysis ID 904)
    use_hfrs
        The Hospital Frailty Risk Score score using all conditions prior
        to the window end. (analysis ID 926)
    use_distinct_condition_count_long_term
        The number of distinct condition concepts observed in the long
        term window. (analysis ID 905)
    use_distinct_condition_count_medium_term
        The number of distinct condition concepts observed in the medium
        term window. (analysis ID 906)
    use_distinct_condition_count_short_term
        The number of distinct condition concepts observed in the short
        term window. (analysis ID 907)
    use_distinct_ingredient_count_long_term
        The number of distinct ingredients observed in the long term
        window. (analysis ID 908)
    use_distinct_ingredient_count_medium_term
        The number of distinct ingredients observed in the medium term
        window. (analysis ID 909)
    use_distinct_ingredient_count_short_term
        The number of distinct ingredients observed in the short term
        window. (analysis ID 910)
    use_distinct_procedure_count_long_term
        The number of distinct procedures observed in the long term
        window. (analysis ID 911)
    use_distinct_procedure_count_medium_term
        The number of distinct procedures observed in the medium term
        window. (analysis ID 912)
    use_distinct_procedure_count_short_term
        The number of distinct procedures observed in the short term
        window. (analysis ID 913)
    use_distinct_measurement_count_long_term
        The number of distinct measurements observed in the long term
        window. (analysis ID 914)
    use_distinct_measurement_count_medium_term
        The number of distinct measurements observed in the medium term
        window. (analysis ID 915)
    use_distinct_measurement_count_short_term
        The number of distinct measurements observed in the short term
        window. (analysis ID 916)
    use_distinct_observation_count_long_term
        The number of distinct observations observed in the long term
        window. (analysis ID 917)
    use_distinct_observation_count_medium_term
        The number of distinct observations observed in the medium term
        window. (analysis ID 918)
    use_distinct_observation_count_short_term
        The number of distinct observations observed in the short term
        window. (analysis ID 919)
    use_visit_count_long_term
        The number of visits observed in the long term window. (analysis
        ID 920)
    use_visit_count_medium_term
        The number of visits observed in the medium term window. (analysis
        ID 921)
    use_visit_count_short_term
        The number of visits observed in the short term window. (analysis
        ID 922)
    use_visit_concept_count_long_term
        The number of visits observed in the long term window, stratified
        by visit concept ID. (analysis ID 923)
    use_visit_concept_count_medium_term
        The number of visits observed in the medium term window,
        stratified by visit concept ID. (analysis ID 924)
    use_visit_concept_count_short_term
        The number of visits observed in the short term window, stratified
        by visit concept ID. (analysis ID 925)
    long_term_start_days
        What is the start day (relative to the index date) of the
        long-term window?
    medium_term_start_days
        What is the start day (relative to the index date) of the
        medium-term window?
    short_term_start_days
        What is the start day (relative to the index date) of the
        short-term window?
    end_days
        What is the end day (relative to the index date) of the window?
    included_covariate_concept_ids
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include
        Should descendant concept IDs be added to the list of concepts to
        include?
    excluded_covariate_concept_ids
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude
        Should descendant concept IDs be added to the list of concepts to
        exclude?
    included_covariate_ids
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> settings = create_covariate_settings(
    ...     use_demographics_gender=True,
    ...     use_demographics_age_group=True,
    ...     use_condition_occurrence_any_time_prior=True
    ... )
    """
    return ListVectorExtended.from_list_vector(
        extractor_r.createCovariateSettings(
            use_demographics_gender,
            use_demographics_age,
            use_demographics_age_group,
            use_demographics_race,
            use_demographics_ethnicity,
            use_demographics_index_year,
            use_demographics_index_month,
            use_demographics_prior_observation_time,
            use_demographics_post_observation_time,
            use_demographics_time_in_cohort,
            use_demographics_index_year_month,
            use_care_site_id,
            use_condition_occurrence_any_time_prior,
            use_condition_occurrence_long_term,
            use_condition_occurrence_medium_term,
            use_condition_occurrence_short_term,
            use_condition_occurrence_primary_inpatient_any_time_prior,
            use_condition_occurrence_primary_inpatient_long_term,
            use_condition_occurrence_primary_inpatient_medium_term,
            use_condition_occurrence_primary_inpatient_short_term,
            use_condition_era_any_time_prior,
            use_condition_era_long_term,
            use_condition_era_medium_term,
            use_condition_era_short_term,
            use_condition_era_overlapping,
            use_condition_era_start_long_term,
            use_condition_era_start_medium_term,
            use_condition_era_start_short_term,
            use_condition_group_era_any_time_prior,
            use_condition_group_era_long_term,
            use_condition_group_era_medium_term,
            use_condition_group_era_short_term,
            use_condition_group_era_overlapping,
            use_condition_group_era_start_long_term,
            use_condition_group_era_start_medium_term,
            use_condition_group_era_start_short_term,
            use_drug_exposure_any_time_prior,
            use_drug_exposure_long_term,
            use_drug_exposure_medium_term,
            use_drug_exposure_short_term,
            use_drug_era_any_time_prior,
            use_drug_era_long_term,
            use_drug_era_medium_term,
            use_drug_era_short_term,
            use_drug_era_overlapping,
            use_drug_era_start_long_term,
            use_drug_era_start_medium_term,
            use_drug_era_start_short_term,
            use_drug_group_era_any_time_prior,
            use_drug_group_era_long_term,
            use_drug_group_era_medium_term,
            use_drug_group_era_short_term,
            use_drug_group_era_overlapping,
            use_drug_group_era_start_long_term,
            use_drug_group_era_start_medium_term,
            use_drug_group_era_start_short_term,
            use_procedure_occurrence_any_time_prior,
            use_procedure_occurrence_long_term,
            use_procedure_occurrence_medium_term,
            use_procedure_occurrence_short_term,
            use_device_exposure_any_time_prior,
            use_device_exposure_long_term,
            use_device_exposure_medium_term,
            use_device_exposure_short_term,
            use_measurement_any_time_prior,
            use_measurement_long_term,
            use_measurement_medium_term,
            use_measurement_short_term,
            use_measurement_value_any_time_prior,
            use_measurement_value_long_term,
            use_measurement_value_medium_term,
            use_measurement_value_short_term,
            use_measurement_range_group_any_time_prior,
            use_measurement_range_group_long_term,
            use_measurement_range_group_medium_term,
            use_measurement_range_group_short_term,
            use_observation_any_time_prior,
            use_observation_long_term,
            use_observation_medium_term,
            use_observation_short_term,
            use_charlson_index,
            use_dcsi,
            use_chads2,
            use_chads2_vasc,
            use_hfrs,
            use_distinct_condition_count_long_term,
            use_distinct_condition_count_medium_term,
            use_distinct_condition_count_short_term,
            use_distinct_ingredient_count_long_term,
            use_distinct_ingredient_count_medium_term,
            use_distinct_ingredient_count_short_term,
            use_distinct_procedure_count_long_term,
            use_distinct_procedure_count_medium_term,
            use_distinct_procedure_count_short_term,
            use_distinct_measurement_count_long_term,
            use_distinct_measurement_count_medium_term,
            use_distinct_measurement_count_short_term,
            use_distinct_observation_count_long_term,
            use_distinct_observation_count_medium_term,
            use_distinct_observation_count_short_term,
            use_visit_count_long_term,
            use_visit_count_medium_term,
            use_visit_count_short_term,
            use_visit_concept_count_long_term,
            use_visit_concept_count_medium_term,
            use_visit_concept_count_short_term,
            long_term_start_days,
            medium_term_start_days,
            short_term_start_days,
            end_days,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/DefaultTemporalCovariateSettings.R
# functions:
#    - createTemporalCovariateSettings (create_temporal_covariate_settings)
# -----------------------------------------------------------------------------
def create_temporal_covariate_settings(
    use_demographics_gender: bool = False,
    use_demographics_age: bool = False,
    use_demographics_age_group: bool = False,
    use_demographics_race: bool = False,
    use_demographics_ethnicity: bool = False,
    use_demographics_index_year: bool = False,
    use_demographics_index_month: bool = False,
    use_demographics_prior_observation_time: bool = False,
    use_demographics_post_observation_time: bool = False,
    use_demographics_time_in_cohort: bool = False,
    use_demographics_index_year_month: bool = False,
    use_care_site_id: bool = False,
    use_condition_occurrence: bool = False,
    use_condition_occurrence_primary_inpatient: bool = False,
    use_condition_era_start: bool = False,
    use_condition_era_overlap: bool = False,
    use_condition_era_group_start: bool = False,
    use_condition_era_group_overlap: bool = False,
    use_drug_exposure: bool = False,
    use_drug_era_start: bool = False,
    use_drug_era_overlap: bool = False,
    use_drug_era_group_start: bool = False,
    use_drug_era_group_overlap: bool = False,
    use_procedure_occurrence: bool = False,
    use_device_exposure: bool = False,
    use_measurement: bool = False,
    use_measurement_value: bool = False,
    use_measurement_range_group: bool = False,
    use_observation: bool = False,
    use_charlson_index: bool = False,
    use_dcsi: bool = False,
    use_chads2: bool = False,
    use_chads2_vasc: bool = False,
    use_hfrs: bool = False,
    use_distinct_condition_count: bool = False,
    use_distinct_ingredient_count: bool = False,
    use_distinct_procedure_count: bool = False,
    use_distinct_measurement_count: bool = False,
    use_distinct_observation_count: bool = False,
    use_visit_count: bool = False,
    use_visit_concept_count: bool = False,
    temporal_start_days: list[int] = list(range(-365, 0, 1)),
    temporal_end_days: list[int] = list(range(-365, 0, 1)),
    included_covariate_concept_ids: list = [],
    add_descendants_to_include: bool = False,
    excluded_covariate_concept_ids: list = [],
    add_descendants_to_exclude: bool = False,
    included_covariate_ids: list = []
) -> ListVectorExtended:
    """
    Create covariate settings

    Creates an object specifying how covariates should be constructed from
    data in the CDM model.

    Wraps the R``FeatureExtraction::createTemporalCovariateSettings`` function
    defined in ``FeatureExtraction/R/DefaultTemporalCovariateSettings.R``

    Parameters
    ----------
    use_demographics_gender
        Gender of the subject. (analysis ID 1)
    use_demographics_age
        Age of the subject on the index date (in years). (analysis ID 2)
    use_demographics_age_group
        Age of the subject on the index date (in 5 year age groups)
        (analysis ID 3)
    use_demographics_race
        Race of the subject. (analysis ID 4)
    use_demographics_ethnicity
        Ethnicity of the subject. (analysis ID 5)
    use_demographics_index_year
        Year of the index date. (analysis ID 6)
    use_demographics_index_month
        Month of the index date. (analysis ID 7)
    use_demographics_prior_observation_time
        Number of days of observation time preceding the index date.
        (analysis ID 8)
    use_demographics_post_observation_time
        Number of days of observation time preceding the index date.
        (analysis ID 9)
    use_demographics_time_in_cohort
        Number of days of observation time preceding the index date.
        (analysis ID 10)
    use_demographics_index_year_month
        Calendar month of the index date. (analysis ID 11)
    use_care_site_id
        Care site associated with the cohort start, pulled from the
        visit_detail, visit_occurrence, or person table, in that order.
        (analysis ID 12)
    use_condition_occurrence
        One covariate per condition in the condition_occurrence table
        starting in the time window. (analysis ID 101)
    use_condition_occurrence_primary_inpatient
        One covariate per condition observed as a primary diagnosis in an
        inpatient setting in the condition_occurrence table starting in the
        time window. (analysis ID 102)
    use_condition_era_start
        One covariate per condition in the condition_era table starting in
        the time window. (analysis ID 201)
    use_condition_era_overlap
        One covariate per condition in the condition_era table overlapping
        with any part of the time window. (analysis ID 202)
    use_condition_era_group_start
        One covariate per condition era rolled up to SNOMED groups in the
        condition_era table starting in the time window. (analysis ID 203)
    use_condition_era_group_overlap
        One covariate per condition era rolled up to SNOMED groups in the
        condition_era table overlapping with any part of the time window.
        (analysis ID 204)
    use_drug_exposure
        One covariate per drug in the drug_exposure table starting in the
        time window. (analysis ID 301)
    use_drug_era_start
        One covariate per drug in the drug_era table starting in the time
        window. (analysis ID 401)
    use_drug_era_overlap
        One covariate per drug in the drug_era table overlapping with any
        part of the time window. (analysis ID 402)
    use_drug_era_group_start
        One covariate per drug rolled up to ATC groups in the drug_era
        table starting in the time window. (analysis ID 403)
    use_drug_era_group_overlap
        One covariate per drug rolled up to ATC groups in the drug_era
        table overlapping with any part of the time window. (analysis
        ID 404)
    use_procedure_occurrence
        One covariate per procedure in the procedure_occurrence table in
        the time window. (analysis ID 501)
    use_device_exposure
        One covariate per device in the device exposure table starting in
        the timewindow. (analysis ID 601)
    use_measurement
        One covariate per measurement in the measurement table in the time
        window. (analysis ID 701)
    use_measurement_value
        One covariate containing the value per measurement-unit combination
        in the time window. If multiple values are found, the last is
        taken. (analysis ID 702)
    use_measurement_range_group
        Covariates indicating whether measurements are below, within, or
        above normal range within the time period. (analysis ID 703)
    use_observation
        One covariate per observation in the observation table in the time
        window. (analysis ID 801)
    use_charlson_index
        The Charlson comorbidity index (Romano adaptation) using all
        conditions prior to the window end. (analysis ID 901)
    use_dcsi
        The Diabetes Comorbidity Severity Index (DCSI) using all
        conditions prior to the window end. (analysis ID 902)
    use_chads2
        The CHADS2 score using all conditions prior to the window end.
        (analysis ID 903)
    use_chads2_vasc
        The CHADS2VASc score using all conditions prior to the window end.
        (analysis ID 904)
    use_hfrs
        The Hospital Frailty Risk Score score using all conditions prior to
        the window end. (analysis ID 926)
    use_distinct_condition_count
        The number of distinct condition concepts observed in the time
        window. (analysis ID 905)
    use_distinct_ingredient_count
        The number of distinct ingredients observed in the time window.
        (analysis ID 906)
    use_distinct_procedure_count
        The number of distinct procedures observed in the time window.
        (analysis ID 907)
    use_distinct_measurement_count
        The number of distinct measurements observed in the time window.
        (analysis ID 908)
    use_distinct_observation_count
        The number of distinct observations in the time window. (analysis
        ID 909)
    use_visit_count
        The number of visits observed in the time window. (analysis ID 910)
    use_visit_concept_count
        The number of visits observed in the time window, stratified by
        visit concept ID. (analysis ID 911)
    temporal_start_days
        A list of integers representing the start of a time period,
        relative to the index date. 0 indicates the index date, -1
        indicates the day before the index date, etc. The start day is
        included in the time period.
    temporal_end_days
        A list of integers representing the end of a time period, relative
        to the index date. 0 indicates the index date, -1 indicates the day
        before the index date, etc. The end day is included in the time
        period.
    included_covariate_concept_ids
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include
        Should descendant concept IDs be added to the list of concepts to
        include?
    excluded_covariate_concept_ids
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude
        Should descendant concept IDs be added to the list of concepts to
        exclude?
    included_covariate_ids
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> settings = create_temporal_covariate_settings(
    ...     use_demographics_gender = True,
    ...     use_demographics_age = True,
    ... )
    """

    # explicit conversion to an Intvector. Else R will convert the list to
    # a generic ListVector
    temporal_start_days = IntVector(temporal_start_days)
    temporal_end_days = IntVector(temporal_end_days)

    return ListVectorExtended.from_list_vector(
        extractor_r.createTemporalCovariateSettings(
            use_demographics_gender,
            use_demographics_age,
            use_demographics_age_group,
            use_demographics_race,
            use_demographics_ethnicity,
            use_demographics_index_year,
            use_demographics_index_month,
            use_demographics_prior_observation_time,
            use_demographics_post_observation_time,
            use_demographics_time_in_cohort,
            use_demographics_index_year_month,
            use_care_site_id,
            use_condition_occurrence,
            use_condition_occurrence_primary_inpatient,
            use_condition_era_start,
            use_condition_era_overlap,
            use_condition_era_group_start,
            use_condition_era_group_overlap,
            use_drug_exposure,
            use_drug_era_start,
            use_drug_era_overlap,
            use_drug_era_group_start,
            use_drug_era_group_overlap,
            use_procedure_occurrence,
            use_device_exposure,
            use_measurement,
            use_measurement_value,
            use_measurement_range_group,
            use_observation,
            use_charlson_index,
            use_dcsi,
            use_chads2,
            use_chads2_vasc,
            use_hfrs,
            use_distinct_condition_count,
            use_distinct_ingredient_count,
            use_distinct_procedure_count,
            use_distinct_measurement_count,
            use_distinct_observation_count,
            use_visit_count,
            use_visit_concept_count,
            temporal_start_days,
            temporal_end_days,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/DefaultTemporalSequenceCovariateSettings.R
# functions:
#    - createTemporalSequenceCovariateSettings
#      (create_temporal_sequence_covariate_settings)
# -----------------------------------------------------------------------------
def create_temporal_sequence_covariate_settings(
    use_demographics_gender: bool = False,
    use_demographics_age: bool = False,
    use_demographics_age_group: bool = False,
    use_demographics_race: bool = False,
    use_demographics_ethnicity: bool = False,
    use_demographics_index_year: bool = False,
    use_demographics_index_month: bool = False,
    use_condition_occurrence: bool = False,
    use_condition_occurrence_primary_inpatient: bool = False,
    use_condition_era_start: bool = False,
    use_condition_era_group_start: bool = False,
    use_drug_exposure: bool = False,
    use_drug_era_start: bool = False,
    use_drug_era_group_start: bool = False,
    use_procedure_occurrence: bool = False,
    use_device_exposure: bool = False,
    use_measurement: bool = False,
    use_measurement_value: bool = False,
    use_observation: bool = False,
    time_part: str = "month",
    time_interval: int = 1,
    sequence_end_day: int = -1,
    sequence_start_day: int = -730,
    included_covariate_concept_ids: list = [],
    add_descendants_to_include: bool = False,
    excluded_covariate_concept_ids: list = [],
    add_descendants_to_exclude: bool = False,
    included_covariate_ids: list = []
) -> ListVectorExtended:
    """
    Create covariate settings

    This function creates an object specifying how covariates should be
    constructed from data in the CDM model.

    Wraps the R ``FeatureExtraction::createTemporalSequenceCovariateSettings``
    function defined in
    ``FeatureExtraction/R/DefaultTemporalCovariateSettings.R``.

    Parameters
    ----------
    use_demographics_gender
        Gender of the subject. (analysis ID 1)
    use_demographics_age
        Age of the subject on the index date (in years). (analysis ID 2)
    use_demographics_age_group
        Age of the subject on the index date (in 5 year age groups)
        (analysis ID 3)
    use_demographics_race
        Race of the subject. (analysis ID 4)
    use_demographics_ethnicity
        Ethnicity of the subject. (analysis ID 5)
    use_demographics_index_year
        Year of the index date. (analysis ID 6)
    use_demographics_index_month
        Month of the index date. (analysis ID 7)
    use_condition_occurrence
        One covariate per condition in the condition_occurrence table
        starting in the time window. (analysis ID 101)
    use_condition_occurrence_primary_inpatient
        One covariate per condition observed as a primary diagnosis in an
        inpatient setting in the condition_occurrence table starting in the
        time window. (analysis ID 102)
    use_condition_era_start
        One covariate per condition in the condition_era table starting in
        the time window. (analysis ID 201)
    use_condition_era_group_start
        One covariate per condition era rolled up to SNOMED groups in the
        condition_era table starting in the time window. (analysis ID 203)
    use_drug_exposure
        One covariate per drug in the drug_exposure table starting in the
        time window. (analysis ID 301)
    use_drug_era_start
        One covariate per drug in the drug_era table starting in the time
        window. (analysis ID 401)
    use_drug_era_group_start
        One covariate per drug rolled up to ATC groups in the
        drug_era table starting in the time window. (analysis ID 403)
    use_procedure_occurrence
        One covariate per procedure in the procedure_occurrence table in
        the time window. (analysis ID 501)
    use_device_exposure
        One covariate per device in the device exposure table starting in
        the time window. (analysis ID 601)
    use_measurement
        One covariate per measurement in the measurement table in the time
        window. (analysis ID 701)
    use_measurement_value
        One covariate containing the value per measurement-unit combination
        in the time window. If multiple values are found, the last is
        taken. (analysis ID 702)
    use_observation
        One covariate per observation in the observation table in the time
        window. (analysis ID 801)
    time_part
        The interval scale ('DAY', 'MONTH', 'YEAR')
    time_interval
        Fixed interval length for timeId using the 'timePart' scale.  For
        example, a 'timePart' of DAY with 'timeInterval' 30 has timeIds
        where timeId 1 is day 0 to day 29, timeId 2 is day 30 to day 59,
        etc.
    sequence_end_day
        What is the end day (relative to the index date) of the data
        extraction?
    sequence_start_day
        What is the start day (relative to the index date) of the data
        extraction?
    included_covariate_concept_ids
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include
        Should descendant concept IDs be added to the list of concepts to
        include?
    excluded_covariate_concept_ids
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude
        Should descendant concept IDs be added to the list of concepts to
        exclude?
    included_covariate_ids
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> settings = create_temporal_sequence_covariate_settings(
    ...     use_demographics_gender = True,
    ...     use_demographics_age = False,
    ...     use_demographics_age_group = True,
    ...     use_demographics_race = True,
    ...     use_demographics_ethnicity = True,
    ...     use_demographics_index_year = True,
    ...     use_demographics_index_month = True,
    ...     use_condition_occurrence = False,
    ...     use_condition_occurrence_primary_inpatient = False,
    ...     use_condition_era_start = False,
    ...     use_condition_era_group_start = False,
    ...     use_drug_exposure = False,
    ...     use_drug_era_start = False,
    ...     use_drug_era_group_start = False,
    ...     use_procedure_occurrence = True,
    ...     use_device_exposure = True,
    ...     use_measurement = True,
    ...     use_measurement_value = False,
    ...     use_observation = True,
    ...     time_part = "DAY",
    ...     time_interval = 1,
    ...     sequence_end_day = -1,
    ...     sequence_start_day = -730,
    ...     included_covariate_concept_ids = [],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = []
    ... )
    """
    return ListVectorExtended.from_list_vector(
        extractor_r.createTemporalSequenceCovariateSettings(
            use_demographics_gender,
            use_demographics_age,
            use_demographics_age_group,
            use_demographics_race,
            use_demographics_ethnicity,
            use_demographics_index_year,
            use_demographics_index_month,
            use_condition_occurrence,
            use_condition_occurrence_primary_inpatient,
            use_condition_era_start,
            use_condition_era_group_start,
            use_drug_exposure,
            use_drug_era_start,
            use_drug_era_group_start,
            use_procedure_occurrence,
            use_device_exposure,
            use_measurement,
            use_measurement_value,
            use_observation,
            time_part,
            time_interval,
            sequence_end_day,
            sequence_start_day,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/DetailedCovariateSettings.R
# functions:
#    - createDefaultCovariateSettings (create_default_covariate_settings)
#    - convertPrespecSettingsToDetailedSettings
#      (convert_prespec_settings_to_detailed_settings)
#    - createAnalysisDetails (create_analysis_details)
#    - createDetailedCovariateSettings (create_detailed_covariate_settings)
#    - createDefaultTemporalCovariateSettings
#      (create_default_temporal_covariate_settings)
#    - createDetailedTemporalCovariateSettings
#      (create_detailed_temporal_covariate_settings)
# -----------------------------------------------------------------------------
def create_default_covariate_settings(
        included_covariate_concept_ids: list[int] = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list[int] = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list[int] = []
        ) -> ListVectorExtended:
    """
    Create default covariate settings

    Wraps the R ``FeatureExtraction::createDefaultCovariateSettings``
    function defined in ``FeatureExtraction/R/DetailedCovariateSettings.R``.

    Parameters
    ----------
    included_covariate_concept_ids : list[int]
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include : bool
        Should descendant concept IDs be added to the list of concepts
        to include?
    excluded_covariate_concept_ids : list[int]
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude : bool
        Should descendant concept IDs be added to the list of concepts
        to exclude?
    included_covariate_ids : list[int]
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> cov_settings = create_default_covariate_settings(
    ...     included_covariate_concept_ids = [1],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [2],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = [1]
    ... )
    """
    return ListVectorExtended.from_list_vector(
        extractor_r.createDefaultCovariateSettings(
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )


def convert_prespec_settings_to_detailed_settings(
        covariate_settings: ListVector | ListVectorExtended
        ) -> ListVectorExtended:
    """
    Convert pre-specified covariate settings to detailed covariate settings

    Wraps the R
    ``FeatureExtraction::convertPrespecSettingsToDetailedSettings``
    function defined in
    ``FeatureExtraction/R/DetailedCovariateSettings.R``.

    Parameters
    ----------
    covariate_settings: ListVector | ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Returns
    -------
    ListVector
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> cov_settings = create_default_covariate_settings(
    ...     included_covariate_concept_ids = [1],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [2],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = [1]
    ... )
    >>> cov_settings = convert_prespec_settings_to_detailed_settings(
    ...     cov_settings
    ... )
    """
    return ListVectorExtended.from_list_vector(
        extractor_r.convertPrespecSettingsToDetailedSettings(
            covariate_settings
        )
    )


def create_analysis_details(
        analysis_id: int, sql_file_name: str, parameters: dict,
        included_covariate_concept_ids: list[int] = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list[int] = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list[int] = []
        ) -> ListVectorExtended:
    """
    Create detailed covariate settings

    Creates an object specifying in detail how covariates should be
    constructed from data in the CDM model. Warning: this function is for
    advanced users only.

    Wraps the R ``FeatureExtraction::createAnalysisDetails`` function
    defined in ``FeatureExtraction/R/DetailedCovariateSettings.R``.

    Parameters
    ----------
    analysis_id : int
        An integer between 0 and 999 that uniquely identifies this
        analysis.
    sql_file_name : str
        The name of the parameterized SQL file embedded in the
        ``featureExtraction`` package.
    parameters : dict
        The list of parameter values used to render the template SQL.
    included_covariate_concept_ids : list[int]
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include : bool
        Should descendant concept IDs be added to the list of concepts
        to include?
    excluded_covariate_concept_ids : list[int]
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude : bool
        Should descendant concept IDs be added to the list of concepts
        to exclude?
    included_covariate_ids : list[int]
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVectorExtended
        An object of type ``analysisDetails``, to be used in other
        functions.

    Examples
    --------
    >>> analysis_details = create_analysis_details(
    ...     analysis_id = 1,
    ...     sql_file_name = "DemographicsGender.sql",
    ...     parameters = {
    ...         analysis_id: 1,
    ...         analysis_name: "Gender",
    ...         domain_id: "Demographics",
    ...     },
    ...     included_covariate_concept_ids = [],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = []
    ... )
    """
    parameters_json = json.dumps(parameters)
    return ListVectorExtended.from_list_vector(
        extractor_r.createAnalysisDetails(
            analysis_id,
            sql_file_name,
            parameters_json,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )


def create_detailed_covariate_settings(analyses: list = []) \
        -> ListVectorExtended:
    """
    Create detailed covariate settings

    Creates an object specifying in detail how covariates should be
    constructed from data in the CDM model. Warning: this function is for
    advanced users only.

    Wraps the R ``FeatureExtraction::createDetailedCovariateSettings``
    function defined in ``FeatureExtraction/R/DetailedCovariateSettings.R``.

    Parameters
    ----------
    analyses: list
        A list of analysis detail objects as created using
        ``createAnalysisDetails``.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> analysis_details = create_analysis_details(
    ...     analysis_id = 1,
    ...     sql_file_name = "DemographicsGender.sql",
    ...     parameters = {
    ...         analysis_id: 1,
    ...         analysis_name: "Gender",
    ...         domain_id: "Demographics",
    ...     },
    ...     included_covariate_concept_ids = [],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = []
    ... )
    >>> cov_settings = create_detailed_covariate_settings(analysis_details)
    """
    return ListVectorExtended.from_list_vector(
        extractor_r.createDetailedCovariateSettings(analyses)
    )


def create_default_temporal_covariate_settings(
        included_covariate_concept_ids: list[int] = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list[int] = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list[int] = []
        ) -> ListVectorExtended:
    """
    Create default temporal covariate settings

    Creates an object specifying in detail how covariates should be
    constructed from data in the CDM model. Warning: this function is for
    advanced users only.

    Wraps the R
    ``FeatureExtraction::createDefaultTemporalCovariateSettings`` function
    defined in ``FeatureExtraction/R/DetailedCovariateSettings.R``.

    Parameters
    ----------
    included_covariate_concept_ids : list[int]
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include : bool
        Should descendant concept IDs be added to the list of concepts
        to include?
    excluded_covariate_concept_ids : list[int]
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude : bool
        Should descendant concept IDs be added to the list of concepts
        to exclude?
    included_covariate_ids : list[int]
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVectorExtended
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> cov_settings = create_default_temporal_covariate_settings(
    ...     included_covariate_concept_ids = [1],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [2],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = [1]
    ... )
    """
    return ListVectorExtended.from_list_vector(
        extractor_r.createDefaultTemporalCovariateSettings(
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )


def create_detailed_temporal_covariate_settings(
        analyses: list = [],
        temporal_start_days: list[int] = list(range(-365, 0, 1)),
        temporal_end_days: list[int] = list(range(-365, 0, 1))
        ) -> ListVectorExtended:
    """
    Create detailed temporal covariate settings

    Creates an object specifying in detail how temporal covariates should
    be constructed from data in the CDM model. Warning: this function is
    for advanced users only.

    Wraps the R ``FeatureExtraction::createDetailedTemporalCovariateSettings``
    function defined in ``FeatureExtraction/R/DetailedCovariateSettings.R``.

    Parameters
    ----------
    analyses : list, optional
        A list of analysis detail objects as created using
        ``createAnalysisDetails``, by default []
    temporal_start_days : list[int], optional
        A list of integers representing the start of a time period,
        relative to the index date. 0 indicates the index date, -1
        indicates the day before the index date, etc. The start day is
        included in the time period., by default range(-365,-1, 1)
    temporal_end_days : list[int], optional
        A list of integers representing the end of a time period, relative
        to the index date. 0 indicates the index date, -1 indicates the day
        before the index date, etc. The end day is included in the time
        period., by default range(-365, -1, 1)

    Returns
    -------
    ListVector
        An object of type ``covariateSettings``, to be used in other
        functions.

    Examples
    --------
    >>> cov_settings = create_detailed_temporal_covariate_settings(
    ...     analyses = analysis_details,
    ...     temporal_start_days = range(-365, 0, 1),
    ...     temporal_end_days = range(-365, 0, 1)
    ... )
    """

    # Explicitly convert to IntVector
    temporal_start_days = IntVector(temporal_start_days)
    temporal_end_days = IntVector(temporal_end_days)

    return ListVectorExtended.from_list_vector(
        extractor_r.createDetailedTemporalCovariateSettings(
            analyses,
            temporal_start_days,
            temporal_end_days
        )
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/GetCovariates.R
# functions:
#    - getDbCovariateData (get_db_covariate_data)
# -----------------------------------------------------------------------------
def get_db_covariate_data(
    cdm_database_schema: str,
    covariate_settings: ListVector,
    connection_details: RS4 | None = None,
    connection: RS4 | None = None,
    oracle_temp_schema: str | None = None,
    cdm_version: str = "5",
    cohort_table: str = "cohort",
    cohort_database_schema: str | None = None,
    cohort_table_is_temp: bool = False,
    cohort_id: int = -1,
    row_id_field: str = "subject_id",
    aggregated: bool = False
) -> CovariateData:
    """
    Get covariate information from the database

    Uses one or several covariate builder functions to construct
    covariates. This function uses the data in the CDM to construct a large
    set of covariates for the provided cohort. The cohort is assumed to be
    in an existing table with these fields: 'subject_id',
    'cohort_definition_id', 'cohort_start_date'. Optionally, an extra field
    can be added containing the unique identifier that will be used as
    rowID in the output.

    Wraps the R ``FeatureExtraction::getDbCovariateData`` function defined
    in ``FeatureExtraction/R/GetCovariates.R``.

    Parameters
    ----------
    connection_details
        An R object of type ``connectionDetails`` created using the
        function ``createConnectionDetails`` in the ``DatabaseConnector``
        package. Either the ``connection`` or ``connectionDetails``
        argument should be specified.
    connection
        A connection to the server containing the schema as created using
        the ``connect`` function in the ``DatabaseConnector`` package.
        Either the ``connection`` or ``connectionDetails`` argument should
        be specified.
    oracle_temp_schema
        A schema where temp tables can be created in Oracle.
    cdm_database_schema
        The name of the database schema that contains the OMOP CDM
        instance. Requires read permissions to this database. On SQL
        Server, this should specify both the database and the schema, so
        for example 'cdm_instance.dbo'.
    cdm_version
        Define the OMOP CDM version used: currently supported is "5".
    cohort_table
        Name of the (temp) table holding the cohort for which we want to
        construct covariates
    cohort_database_schema
        If the cohort table is not a temp table, specify the database
        schema where the cohort table can be found. On SQL Server, this
        should specify both the database and the schema, so for example
        'cdm_instance.dbo'.
    cohort_table_is_temp
        Is the cohort table a temp table?
    cohort_id
        For which cohort ID(s) should covariates be constructed? If set to
        -1, covariates will be constructed for all cohorts in the specified
        cohort table.
    row_id_field
        The name of the field in the cohort table that is to be used as the
        row_id field in the output table. This can be especially useful if
        there is more than one period per person.
    covariate_settings
        Either an object of type ``covariateSettings`` as created using one
        of the createCovariate functions, or a list of such objects.
    aggregated
        Should aggregate statistics be computed instead of covariates per
        cohort entry?

    Returns
    -------
    CovariateData
        Returns an object of type ``covariateData``, containing information
        on the covariates.

    Examples
    --------
    >>> cov_data = get_db_covariate_data(
    ...     connection_details = connection_details,
    ...     oracle_temp_schema = None,
    ...     cdm_database_schema = "main",
    ...     cdm_version = "5",
    ...     cohort_table = "cohort",
    ...     cohort_database_schema = "main",
    ...     cohort_table_is_temp = False,
    ...     cohort_id = -1,
    ...     row_id_field = "subject_id",
    ...     covariate_settings = cov_settings,
    ...     aggregated = False
    ... )
    """
    # filter non args
    args = {
        "connectionDetails": connection_details,
        "connection": connection,
        "oracleTempSchema": oracle_temp_schema,
        "cdmDatabaseSchema": cdm_database_schema,
        "cdmVersion": cdm_version,
        "cohortTable": cohort_table,
        "cohortDatabaseSchema": cohort_database_schema,
        "cohortTableIsTemp": cohort_table_is_temp,
        "cohortId": cohort_id,
        "rowIdField": row_id_field,
        "covariateSettings": covariate_settings,
        "aggregated": aggregated
    }

    # remove None values
    args = {k: v for k, v in args.items() if v is not None}

    return CovariateData.from_RS4(extractor_r.getDbCovariateData(**args))


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/GetDefaultCovariates.R
# functions:
#    - getDbDefaultCovariateData (get_db_default_covariate_data)
# -----------------------------------------------------------------------------
def get_db_default_covariate_data(
    cdm_database_schema: str,
    covariate_settings: ListVector | ListVectorExtended | None = None,
    target_database_schema: str | None = None,
    target_covariate_table: str | None = None,
    target_covariate_ref_table: str | None = None,
    target_analysis_ref_table: str | None = None,
    connection: RS4 | None = None,
    oracle_temp_schema: str | None = None,
    cohort_table: str = "#cohort_person",
    cohort_id: int = -1,
    cdm_version: str = "5",
    row_id_field: str = "subject_id",
    aggregated: bool = False
) -> CovariateData:
    """
    Get default covariate information from the database

    Constructs a large default set of covariates for one or more cohorts
    using data in the CDM schema. Includes covariates for all drugs, drug
    classes, condition, condition classes, procedures, observations, etc.

    Wraps the R ``FeatureExtraction::getDbDefaultCovariateData`` function
    defined in ``FeatureExtraction/R/GetDefaultCovariates.R``.

    Parameters
    ----------
    cdm_database_schema : str
        The name of the database schema that contains the OMOP CDM
        instance.
    covariate_settings : ListVector | ListVectorExtended
        Either an object of type ``covariateSettings`` as created using one
        of the createCovariate functions, or a list of such objects.
    target_database_schema (Optional)
        The name of the database schema where the resulting covariates
        should be stored.
    target_covariate_table (Optional)
        The name of the table where the resulting covariates will be
        stored. If not provided, results will be fetched to R. The table
        can be a permanent table in the ``targetDatabaseSchema`` or a temp
        table. If it is a temp table, do not specify
        ``targetDatabaseSchema``.
    target_covariate_ref_table (Optional)
        The name of the table where the covariate reference will be stored.
    target_analysis_ref_table (Optional)
        The name of the table where the analysis reference will be stored.
    connection : RS4 (Optional)
        A connection to the OMOP CDM, as generated by
        ``DatabaseConnector.connect``.
    oracle_temp_schema (Optional)
        The name of the schema where the temp tables should be created.
        This is only relevant for Oracle.
    cohort_table (Optional)
        The name of the (temp) table holding the cohort for which we want
        to construct covariates.
    cohort_id (Optional)
        The ID of the cohort for which we want to construct covariates. If
        set to -1, covariates will be constructed for all cohorts in the
        specified cohort table.
    cdm_version (Optional)
        The version of the CDM. Can be "4" or "5".
    row_id_field (Optional)
        The name of the field in the cohort table that is to be used as
        the row_id field in the output table.
    aggregated (Optional)
        Should aggregate statistics be computed instead of covariates per
        cohort entry?

    Returns
    -------
    CovariateData
        An object of class ``covariateData``.

    Examples
    --------
    >>> results = get_db_default_covariate_data(
    ...     connection = connection,
    ...     cdm_database_schema = "main",
    ...     cohort_table = "cohort",
    ...     covariate_settings = create_default_covariate_settings(),
    ...     target_database_schema = "main",
    ...     target_covariate_table = "ut_cov",
    ...     target_covariate_ref_table = "ut_cov_ref",
    ...     target_analysis_ref_table = "ut_cov_analysis_ref"
    ... )
    """
    if covariate_settings is None:
        covariate_settings = create_default_covariate_settings()

    # filter non args
    args = {
        "cdmDatabaseSchema": cdm_database_schema,
        "targetDatabaseSchema": target_database_schema,
        "targetCovariateTable": target_covariate_table,
        "targetCovariateRefTable": target_covariate_ref_table,
        "targetAnalysisRefTable": target_analysis_ref_table,
        "covariateSettings": covariate_settings,
        "connection": connection,
        "oracleTempSchema": oracle_temp_schema,
        "cohortTable": cohort_table,
        "cohortId": cohort_id,
        "cdmVersion": cdm_version,
        "rowIdField": row_id_field,
        "aggregated": aggregated
    }

    # remove None values
    args = {k: v for k, v in args.items() if v is not None}

    return CovariateData.from_RS4(
        extractor_r.getDbDefaultCovariateData(**args)
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/HelperFunctions.R
# functions:
#    - filterByRowId (filter_by_row_id)
#    - filterByCohortDefinitionId (filter_by_cohort_definition_id)
# -----------------------------------------------------------------------------
def filter_by_row_id(covariate_data: RS4 | CovariateData, row_ids: list[int]) \
        -> CovariateData:
    """
    Filter covariates by row ID

    Wraps the R ``FeatureExtraction::filterByRowId`` function defined in
    ``FeatureExtraction/R/HelperFunctions.R``.

    Parameters
    ----------
    covariate_data : RS4 | CovariateData
        An object of type ``CovariateData``.
    row_ids : list[int]
        A vector containing the row_ids to keep.

    Returns
    -------
    CovariateData
        An object of type ``CovariateData``.

    Examples
    --------
    >>> covariate_data <- filter_by_row_id(
    ...     covariate_data = covariate_data,
    ...     row_ids = [1,2]
    ... )
    """
    row_ids_list = IntVector(row_ids)
    return CovariateData.from_RS4(
        extractor_r.filterByRowId(covariate_data, row_ids_list)
    )


def filter_by_cohort_definition_id(covariate_data: RS4 | CovariateData,
                                   cohort_id: int) -> CovariateData:
    """
    Filter covariates by cohort definition ID

    Wraps the R ``FeatureExtraction::filterByCohortDefinitionId`` function
    defined in ``FeatureExtraction/R/HelperFunctions.R``.

    Parameters
    ----------
    covariate_data : RS4 | CovariateData
        An object of type ``CovariateData``.
    cohort_id : int
        The cohort definition ID to keep.

    Returns
    -------
    CovariateData
        An object of type ``CovariateData``.

    Examples
    --------
    >>> covariate_data = filter_by_cohort_definition_id(
    ...     covariate_data = covariate_data,
    ...     cohort_id = 1
    ... )
    """
    return CovariateData.from_RS4(
        extractor_r.filterByCohortDefinitionId(covariate_data, cohort_id)
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/Normalization.R
# functions:
#    - tidyCovariateData (tidy_covariate_data)
# -----------------------------------------------------------------------------
def tidy_covariate_data(covariate_data: RS4 | CovariateData,
                        min_fraction: float = 0.001, normalize: bool = True,
                        remove_redundancy: bool = True) -> CovariateData:
    """
    Tidy covariate data

    Normalize covariate values by dividing by the max and/or remove
    redundant covariates and/or remove infrequent covariates. For temporal
    covariates, redundancy is evaluated per time ID.

    Wraps the R ``FeatureExtraction::tidyCovariateData`` function defined in
    ``FeatureExtraction/R/Normalization.R``.

    Parameters
    ----------
    covariate_data : RS4 | CovariateData
        An object as generated using the ``getDbCovariateData`` function.
    min_fraction : float
        Minimum fraction of the population that should have a non-zero
        value for a covariate for that covariate to be kept. Set to 0 to
        don't filter on frequency.
    normalize : bool
        Normalize the covariates? (dividing by the max).
    remove_redundancy : bool
        Should redundant covariates be removed?

    Returns
    -------
    CovariateData
        An object of class ``covariateData``.

    Examples
    --------
    >>> covariate_data = tidy_covariate_data(
    ...     covariate_data = covariate_data,
    ...     min_fraction = 0.001,
    ...     normalize = True,
    ...     removeRedundancy = True
    ... )
    """
    return CovariateData.from_RS4(
        extractor_r.tidyCovariateData(
            covariate_data, min_fraction, normalize, remove_redundancy
        )
    )


# -----------------------------------------------------------------------------
# wrapper: FeatureExtraction/R/Table1.R
# functions:
#    - getDefaultTable1Specifications (get_default_table1_specifications)
#    - createTable1 (create_table1)
#    - createTable1FromCovariateSettings
#      (create_table1_from_covariate_settings)
# -----------------------------------------------------------------------------
def get_default_table1_specifications() -> DataFrame:
    """
    Get the default table 1 specifications

    Loads the default specifications for a table 1, to be used with the
    ``createTable1`` function.

    Wraps the R ``FeatureExtraction::getDefaultTable1Specifications`` function
    defined in ``FeatureExtraction/R/Table1.R``.

    Returns
    -------
    DataFrame
        Returns a ``specifications`` DataFrame.

    Examples
    --------
    >>> default_table1_specs = Table1.get_default_table1_specifications()
    """
    return extractor_r.getDefaultTable1Specifications()


def create_table1(covariate_data1: RS4, covariate_data2: RS4 | None = None,
                  cohort_id1: int | None = None, cohort_id2: int | None = None,
                  specifications: DataFrame | None = None,
                  output: str = "two columns", show_counts: bool = False,
                  show_percent: bool = True,
                  percent_digits: int = 1, value_digits: int = 1,
                  std_diff_digits: int = 2) -> DataFrame | list[DataFrame]:
    """
    Create a table 1

    Creates a formatted table of cohort characteristics, to be included in
    publications or reports. Allows for creating a table describing a
    single cohort, or a table comparing two cohorts.

    Wraps the R ``FeatureExtraction::createTable1`` function defined in
    ``FeatureExtraction/R/Table1.R``.

    Parameters
    ----------
    covariate_data1 : RS4
        The covariate data of the cohort to be included in the table.
    covariate_data2 : RS4
        The covariate data of the cohort to also be included, when
        comparing two cohorts.
    cohort_id1 : int
        If provided, ``covariateData1`` will be restricted to this cohort.
        If not provided, ``covariateData1`` is assumed to contain data on
        only 1 cohort.
    cohort_id2 : int
        If provided, ``covariateData2`` will be restricted to this cohort.
        If not provided, ``covariateData2`` is assumed to contain data on
        only 1 cohort.
    specifications : DataFrame
        Specifications of which covariates to display, and how.
    output : str
        The output format for the table.
        Options are:
        ``output = "two columns"``,
        ``output = "one column"``, or
        ``output = "list"``
    sho_counts : bool
        Show the number of cohort entries having the binary covariate?
    show_percent : bool
        Show the percentage of cohort entries having the binary covariate?
    percent_digits : int
        Number of digits to be used for percentages.
    std_diff_digits : int
        Number of digits to be used for the standardized differences.
    value_digits : int
        Number of digits to be used for the values of continuous variables.

    Returns
    -------
    DataFrame
        A data frame, or, when ``output = "list"`` a list of two data
        frames.

    Examples
    --------
    >>> cov_data1 = get_db_covariate_data(
    ...     connection_details = connection_details,
    ...     cdm_database_schema = "main",
    ...     cohort_table = "cohorts_of_interest",
    ...     cohort_database_schema = "results",
    ...     cohort_id = 1,
    ...     covariate_settings = covariate_settings,
    ...     aggregated = True
    ... )

    >>> cov_data2 = get_db_covariate_data(
    ...     connection_details = connection_details,
    ...     cdm_database_schema = "main",
    ...     cohort_table = "cohorts_of_interest",
    ...     cohort_database_schema = "results",
    ...     cohort_id = 2,
    ...     covariate_settings = covariate_settings,
    ...     aggregated = True
    ... )

    >>> table1 = create_table1(
    ...     covariate_data1 = cov_data1,
    ...     covariate_data2 = cov_data2,
    ...     cohort_id1 = 1,
    ...     cohort_id2 = 2,
    ...     specifications = Table1.get_default_table1_specifications(),
    ...     output = "one column",
    ...     show_counts = False,
    ...     show_percent = TRUE,
    ...     percent_digits = 1,
    ...     value_digits = 1,
    ...     std_diff_digits = 2
    ... )
    """
    if not specifications:
        specifications = get_default_table1_specifications()

    return extractor_r.createTable1(covariate_data1, covariate_data2,
                                    cohort_id1, cohort_id2, specifications,
                                    output, show_counts, show_percent,
                                    percent_digits, value_digits,
                                    std_diff_digits)


def create_table1_covariate_settings(
    specifications: DataFrame | None = None,
    covariate_settings: ListVector | ListVectorExtended | None = None,
    included_covariate_concept_ids: list[int] = [],
    add_descendants_to_include: bool = False,
    excluded_covariate_concept_ids: list[int] = [],
    add_descendants_to_exclude: bool = False,
    included_covariate_ids: list[int] = []
) -> ListVector:
    """
    Create covariate settings for a table 1

    Creates a covariate settings object for generating only those
    covariates that will be included in a table 1. This function works by
    filtering the ``covariateSettings`` object for the covariates in
    ``specifications`` object.

    Wraps the R ``FeatureExtraction::createTable1CovariateSettings``
    function defined in ``FeatureExtraction/R/Table1.R``.

    Parameters
    ----------
    specifications : DataFrame
        A specifications object for generating a table using the
        ``createTable1`` function.
    covariate_settings : ListVector
        The covariate settings object to use as the basis for the filtered
        covariate settings.
    included_covariate_concept_ids : list[int]
        A list of concept IDs that should be used to construct covariates.
    add_descendants_to_include : bool
        Should descendant concept IDs be added to the list of concepts to
        include?
    excluded_covariate_concept_ids : list[int]
        A list of concept IDs that should NOT be used to construct
        covariates.
    add_descendants_to_exclude : bool
        Should descendant concept IDs be added to the list of concepts to
        exclude?
    included_covariate_ids : list[int]
        A list of covariate IDs that should be restricted to.

    Returns
    -------
    ListVector
        A covariate settings object, for example to be used when calling
        the ``getDbCovariateData`` function.

    Examples
    --------
    >>> table1_cov_settings = Table1.create_table1_covariate_settings(
    ...     specifications = Table1.get_default_table1_specifications(),
    ...     included_covariate_concept_ids = [],
    ...     add_descendants_to_include = False,
    ...     excluded_covariate_concept_ids = [],
    ...     add_descendants_to_exclude = False,
    ...     included_covariate_ids = []
    ... )
    """
    if not specifications:
        specifications = get_default_table1_specifications()

    if not covariate_settings:
        covariate_settings = \
            create_default_covariate_settings()

    return ListVectorExtended.from_list_vector(
        extractor_r.createTable1CovariateSettings(
            specifications,
            covariate_settings,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )
    )
