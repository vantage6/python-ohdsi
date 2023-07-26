import os
import json

from rpy2 import robjects
from rpy2.robjects.methods import RS4
from rpy2.robjects.vectors import ListVector

from rpy2.robjects.packages import importr


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


class DefaultCovariateSettings:

    @staticmethod
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
    ) -> ListVector:
        """
        Create covariate settings

        creates an object specifying how covariates should be constructed
        from data in the CDM model.

        Parameters
        ----------
        use_demographics_gender: bool
            Gender of the subject. (analysis ID 1)
        use_demographics_age: bool
            Age of the subject in years at the index date. (analysis ID 2)
        use_demographics_age_group: bool
            Age group of the subject at the index date. (analysis ID 3)
        useDemographicsRace
            Race of the subject. (analysis ID 4)
        useDemographicsEthnicity
            Ethnicity of the subject. (analysis ID 5)
        useDemographicsIndexYear
            Year of the index date. (analysis ID 6)
        useDemographicsIndexMonth
            Month of the index date. (analysis ID 7)
        useDemographicsPriorObservationTime
            Number of continuous days of observation time preceding the index
            date. (analysis ID 8)
        useDemographicsPostObservationTime
            Number of continuous days of observation time following the index
            date. (analysis ID 9)
        useDemographicsTimeInCohort
            Number of days of observation time during cohort period. (analysis
            ID 10)
        useDemographicsIndexYearMonth
            Both calendar year and month of the index date in a single
            variable. (analysis ID 11)
        useCareSiteId
            Care site associated with the cohort start, pulled from the
            visit_detail, visit_occurrence, or person table, in that order.
            (analysis ID 12)
        useConditionOccurrenceAnyTimePrior
            One covariate per condition in the condition_occurrence table
            starting any time prior to index. (analysis ID 101)
        useConditionOccurrenceLongTerm
            One covariate per condition in the condition_occurrence table
            starting in the long term window. (analysis ID 102)
        useConditionOccurrenceMediumTerm
            One covariate per condition in the condition_occurrence table
            starting in the medium term window. (analysis ID 103)
        useConditionOccurrenceShortTerm
            One covariate per condition in the condition_occurrence table
            starting in the short term window. (analysis ID 104)
        useConditionOccurrencePrimaryInpatientAnyTimePrior
            One covariate per condition observed as a primary diagnosis in an
            inpatient setting in the condition_occurrence table starting any
            time prior to index. (analysis ID 105)
        useConditionOccurrencePrimaryInpatientLongTerm
            One covariate per condition observed as a primary diagnosis in an
            inpatient setting in the condition_occurrence table starting in
            the long term window. (analysis ID 106)
        useConditionOccurrencePrimaryInpatientMediumTerm
            One covariate per condition observed as a primary diagnosis in an
            inpatient setting in the condition_occurrence table starting in
            the medium term window. (analysis ID 107)
        useConditionOccurrencePrimaryInpatientShortTerm
            One covariate per condition observed as a primary diagnosis in an
            inpatient setting in the condition_occurrence table starting in
            the short term window. (analysis ID 108)
        useConditionEraAnyTimePrior
            One covariate per condition in the condition_era table overlapping
            with any time prior to index. (analysis ID 201)
        useConditionEraLongTerm
            One covariate per condition in the condition_era table overlapping
            with any part of the long term window. (analysis ID 202)
        useConditionEraMediumTerm
            One covariate per condition in the condition_era table overlapping
            with any part of the medium term window. (analysis ID 203)
        useConditionEraShortTerm
            One covariate per condition in the condition_era table overlapping
            with any part of the short term window. (analysis ID 204)
        useConditionEraOverlapping
            One covariate per condition in the condition_era table overlapping
            with the end of the risk window. (analysis ID 205)
        useConditionEraStartLongTerm
            One covariate per condition in the condition_era table starting in
            the long term window. (analysis ID 206)
        useConditionEraStartMediumTerm
            One covariate per condition in the condition_era table starting in
            the medium term window. (analysis ID 207)
        useConditionEraStartShortTerm
            One covariate per condition in the condition_era table starting in
            the short term window. (analysis ID 208)
        useConditionGroupEraAnyTimePrior
            One covariate per condition era rolled up to groups in the
            condition_era table overlapping with any time prior to index.
            (analysis ID 209)
        useConditionGroupEraLongTerm
            One covariate per condition era rolled up to groups in the
            condition_era table overlapping with any part of the long term
            window. (analysis ID 210)
        useConditionGroupEraMediumTerm
            One covariate per condition era rolled up to groups in the
            condition_era table overlapping with any part of the medium term
            window. (analysis ID 211)
        useConditionGroupEraShortTerm
            One covariate per condition era rolled up to groups in the
            condition_era table overlapping with any part of the short term
            window. (analysis ID 212)
        useConditionGroupEraOverlapping
            One covariate per condition era rolled up to groups in the
            condition_era table overlapping with the end of the risk window.
            (analysis ID 213)
        useConditionGroupEraStartLongTerm
            One covariate per condition era rolled up to groups in the
            condition_era table starting in the long term window. (analysis ID
            214)
        useConditionGroupEraStartMediumTerm
            One covariate per condition era rolled up to groups in the
            condition_era table starting in the medium term window. (analysis
            ID 215)
        useConditionGroupEraStartShortTerm
            One covariate per condition era rolled up to groups in the
            condition_era table starting in the short term window. (analysis
            ID 216)
        useDrugExposureAnyTimePrior
            One covariate per drug in the drug_exposure table starting any
            time prior to index. (analysis ID 301)
        useDrugExposureLongTerm
            One covariate per drug in the drug_exposure table starting in the
            long term window. (analysis ID 302)
        useDrugExposureMediumTerm
            One covariate per drug in the drug_exposure table starting in the
            medium term window. (analysis ID 303)
        useDrugExposureShortTerm
            One covariate per drug in the drug_exposure table starting in the
            short term window. (analysis ID 304)
        useDrugEraAnyTimePrior
            One covariate per drug in the drug_era table overlapping with any
            time prior to index. (analysis ID 401)
        useDrugEraLongTerm
            One covariate per drug in the drug_era table overlapping with any
            part of the long term window. (analysis ID 402)
        useDrugEraMediumTerm
            One covariate per drug in the drug_era table overlapping with any
            part of the medium term window. (analysis ID 403)
        useDrugEraShortTerm
            One covariate per drug in the drug_era table overlapping with any
            part of the short window. (analysis ID 404)
        useDrugEraOverlapping
            One covariate per drug in the drug_era table overlapping with the
            end of the risk window. (analysis ID 405)
        useDrugEraStartLongTerm
            One covariate per drug in the drug_era table starting in the long
            term window. (analysis ID 406)
        useDrugEraStartMediumTerm
            One covariate per drug in the drug_era table starting in the
            medium term window. (analysis ID 407)
        useDrugEraStartShortTerm
            One covariate per drug in the drug_era table starting in the long
            short window. (analysis ID 408)
        useDrugGroupEraAnyTimePrior
            One covariate per drug rolled up to ATC groups in the drug_era
            table overlapping with any time prior to index. (analysis ID 409)
        useDrugGroupEraLongTerm
            One covariate per drug rolled up to ATC groups in the drug_era
            table overlapping with any part of the long term window.
            (analysis ID 410)
        useDrugGroupEraMediumTerm
            One covariate per drug rolled up to ATC groups in the drug_era
            table overlapping with any part of the medium term window.
            (analysis ID 411)
        useDrugGroupEraShortTerm
            One covariate per drug rolled up to ATC groups in the drug_era
            table overlapping with any part of the short term window.
            (analysis ID 412)
        useDrugGroupEraOverlapping
            One covariate per drug rolled up to ATC groups in the drug_era
            table overlapping with the end of the risk window. (analysis ID
            413)
        useDrugGroupEraStartLongTerm
            One covariate per drug rolled up to ATC groups in the drug_era
            table starting in the long term window. (analysis ID 414)
        useDrugGroupEraStartMediumTerm
            One covariate per drug rolled up to ATC groups in the drug_era
            table starting in the medium term window. (analysis ID 415)
        useDrugGroupEraStartShortTerm
            One covariate per drug rolled up to ATC groups in the drug_era
            table starting in the short term window. (analysis ID 416)
        useProcedureOccurrenceAnyTimePrior
            One covariate per procedure in the procedure_occurrence table any
            time prior to index. (analysis ID 501)
        useProcedureOccurrenceLongTerm
            One covariate per procedure in the procedure_occurrence table in
            the long term window. (analysis ID 502)
        useProcedureOccurrenceMediumTerm
            One covariate per procedure in the procedure_occurrence table in
            the medium term window. (analysis ID 503)
        useProcedureOccurrenceShortTerm
            One covariate per procedure in the procedure_occurrence table in
            the short term window. (analysis ID 504)
        useDeviceExposureAnyTimePrior
            One covariate per device in the device exposure table starting any
            time prior to index. (analysis ID 601)
        useDeviceExposureLongTerm
            One covariate per device in the device exposure table starting in
            the long term window. (analysis ID 602)
        useDeviceExposureMediumTerm
            One covariate per device in the device exposure table starting in
            the medium term window. (analysis ID 603)
        useDeviceExposureShortTerm
            One covariate per device in the device exposure table starting in
            the short term window. (analysis ID 604)
        useMeasurementAnyTimePrior
            One covariate per measurement in the measurement table any time
            prior to index. (analysis ID 701)
        useMeasurementLongTerm
            One covariate per measurement in the measurement table in the long
            term window. (analysis ID 702)
        useMeasurementMediumTerm
            One covariate per measurement in the measurement table in the
            medium term window. (analysis ID 703)
        useMeasurementShortTerm
            One covariate per measurement in the measurement table in the
            short term window. (analysis ID 704)
        useMeasurementValueAnyTimePrior
            One covariate containing the value per measurement-unit
            combination any time prior to index. (analysis ID 705)
        useMeasurementValueLongTerm
            One covariate containing the value per measurement-unit
            combination in the long term window. (analysis ID 706)
        useMeasurementValueMediumTerm
            One covariate containing the value per measurement-unit
            combination in the medium term window. (analysis ID 707)
        useMeasurementValueShortTerm
            One covariate containing the value per measurement-unit
            combination in the short term window. (analysis ID 708)
        useMeasurementRangeGroupAnyTimePrior
            Covariates indicating whether measurements are below, within, or
            above normal range any time prior to index. (analysis ID 709)
        useMeasurementRangeGroupLongTerm
            Covariates indicating whether measurements are below, within, or
            above normal range in the long term window. (analysis ID 710)
        useMeasurementRangeGroupMediumTerm
            Covariates indicating whether measurements are below, within, or
            above normal range in the medium term window. (analysis ID 711)
        useMeasurementRangeGroupShortTerm
            Covariates indicating whether measurements are below, within, or
            above normal range in the short term window. (analysis ID 712)
        useObservationAnyTimePrior
            One covariate per observation in the observation table any time
            prior to index. (analysis ID 801)
        useObservationLongTerm
            One covariate per observation in the observation table in the long
            term window. (analysis ID 802)
        useObservationMediumTerm
            One covariate per observation in the observation table in the
            medium term window. (analysis ID 803)
        useObservationShortTerm
            One covariate per observation in the observation table in the
            short term window. (analysis ID 804)
        useCharlsonIndex
            The Charlson comorbidity index (Romano adaptation) using all
            conditions prior to the window end. (analysis ID 901)
        useDcsi
            The Diabetes Comorbidity Severity Index (DCSI) using all
            conditions prior to the window end. (analysis ID 902)
        useChads2
            The CHADS2 score using all conditions prior to the window end.
            (analysis ID 903)
        useChads2Vasc
            The CHADS2VASc score using all conditions prior to the window end.
            (analysis ID 904)
        useHfrs
            The Hospital Frailty Risk Score score using all conditions prior
            to the window end. (analysis ID 926)
        useDistinctConditionCountLongTerm
            The number of distinct condition concepts observed in the long
            term window. (analysis ID 905)
        useDistinctConditionCountMediumTerm
            The number of distinct condition concepts observed in the medium
            term window. (analysis ID 906)
        useDistinctConditionCountShortTerm
            The number of distinct condition concepts observed in the short
            term window. (analysis ID 907)
        useDistinctIngredientCountLongTerm
            The number of distinct ingredients observed in the long term
            window. (analysis ID 908)
        useDistinctIngredientCountMediumTerm
            The number of distinct ingredients observed in the medium term
            window. (analysis ID 909)
        useDistinctIngredientCountShortTerm
            The number of distinct ingredients observed in the short term
            window. (analysis ID 910)
        useDistinctProcedureCountLongTerm
            The number of distinct procedures observed in the long term
            window. (analysis ID 911)
        useDistinctProcedureCountMediumTerm
            The number of distinct procedures observed in the medium term
            window. (analysis ID 912)
        useDistinctProcedureCountShortTerm
            The number of distinct procedures observed in the short term
            window. (analysis ID 913)
        useDistinctMeasurementCountLongTerm
            The number of distinct measurements observed in the long term
            window. (analysis ID 914)
        useDistinctMeasurementCountMediumTerm
            The number of distinct measurements observed in the medium term
            window. (analysis ID 915)
        useDistinctMeasurementCountShortTerm
            The number of distinct measurements observed in the short term
            window. (analysis ID 916)
        useDistinctObservationCountLongTerm
            The number of distinct observations observed in the long term
            window. (analysis ID 917)
        useDistinctObservationCountMediumTerm
            The number of distinct observations observed in the medium term
            window. (analysis ID 918)
        useDistinctObservationCountShortTerm
            The number of distinct observations observed in the short term
            window. (analysis ID 919)
        useVisitCountLongTerm
            The number of visits observed in the long term window. (analysis
            ID 920)
        useVisitCountMediumTerm
            The number of visits observed in the medium term window. (analysis
            ID 921)
        useVisitCountShortTerm
            The number of visits observed in the short term window. (analysis
            ID 922)
        useVisitConceptCountLongTerm
            The number of visits observed in the long term window, stratified
            by visit concept ID. (analysis ID 923)
        useVisitConceptCountMediumTerm
            The number of visits observed in the medium term window,
            stratified by visit concept ID. (analysis ID 924)
        useVisitConceptCountShortTerm
            The number of visits observed in the short term window, stratified
            by visit concept ID. (analysis ID 925)
        longTermStartDays
            What is the start day (relative to the index date) of the
            long-term window?
        mediumTermStartDays
            What is the start day (relative to the index date) of the
            medium-term window?
        shortTermStartDays
            What is the start day (relative to the index date) of the
            short-term window?
        endDays
            What is the end day (relative to the index date) of the window?
        includedCovariateConceptIds
            A list of concept IDs that should be used to construct covariates.
        addDescendantsToInclude
            Should descendant concept IDs be added to the list of concepts to
            include?
        excludedCovariateConceptIds
            A list of concept IDs that should NOT be used to construct
            covariates.
        addDescendantsToExclude
            Should descendant concept IDs be added to the list of concepts to
            exclude?
        includedCovariateIds
            A list of covariate IDs that should be restricted to.

        Returns
        -------
        ListVector
            An object of type ``covariateSettings``, to be used in other
            functions.

        Examples
        --------
        >>> settings = DefaultCovariateSettings.create_covariate_settings(
        ...     use_demographics_gender=True,
        ...     use_demographics_age_group=True,
        ...     use_condition_occurrence_any_time_prior=True
        ... )
        """
        return extractor_r.createCovariateSettings(
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


class DetailedCovariateSettings:

    @staticmethod
    def create_default_covariate_settings(
        included_covariate_concept_ids: list = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list = []
    ) -> ListVector:
        """
        Create default covariate settings

        Parameters
        ----------
        included_covariate_concept_ids
            A list of concept IDs that should be used to construct covariates.
        add_descendants_to_include
            Should descendant concept IDs be added to the list of concepts
            to include?
        excluded_covariate_concept_ids
            A list of concept IDs that should NOT be used to construct
            covariates.
        add_descendants_to_exclude
            Should descendant concept IDs be added to the list of concepts
            to exclude?
        included_covariate_ids
            A list of covariate IDs that should be restricted to.

        Returns
        -------
        ListVector
            An object of type ``covariateSettings``, to be used in other
            functions.

        Examples
        --------
        >>> covSettings <- create_default_covariate_settings(
        ...     included_covariate_concept_ids = [1],
        ...     add_descendants_to_include = False,
        ...     excluded_covariate_concept_ids = [2],
        ...     add_descendants_to_exclude = False,
        ...     included_covariate_ids = [1]
        ... )
        """
        return extractor_r.createDefaultCovariateSettings(
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )

    @staticmethod
    def convert_prespec_settings_to_detailed_settings(
        covariate_settings: ListVector
    ) -> ListVector:
        """
        Convert pre-specified covariate settings to detailed covariate settings

        Parameters
        ----------
        covariate_settings
            An object of type ``covariateSettings``, to be used in other
            functions.

        Returns
        -------
        ListVector
            An object of type ``covariateSettings``, to be used in other
            functions.

        Examples
        --------
        >>> covSettings <- create_default_covariate_settings(
        ...     included_covariate_concept_ids = [1],
        ...     add_descendants_to_include = False,
        ...     excluded_covariate_concept_ids = [2],
        ...     add_descendants_to_exclude = False,
        ...     included_covariate_ids = [1]
        ... )
        >>> covSettings <- convert_prespec_settings_to_detailed_settings(
        ...     covSettings
        ... )
        """
        return extractor_r.convertPrespecSettingsToDetailedSettings(
            covariate_settings
        )

    @staticmethod
    def create_analysis_details(
        analysis_id: int, sql_file_name: str, parameters: dict,
        included_covariate_concept_ids: list = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list = []
    ) -> ListVector:
        """
        Create detailed covariate settings

        creates an object specifying in detail how covariates should be
        constructed from data in the CDM model. Warning: this function is for
        advanced users only.

        Parameters
        ----------
        analysis_id
            An integer between 0 and 999 that uniquely identifies this
            analysis.
        sql_file_name
            The name of the parameterized SQL file embedded in the
            ``featureExtraction`` package.
        parameters
            The list of parameter values used to render the template SQL.
        included_covariate_concept_ids
            A list of concept IDs that should be used to construct covariates.
        add_descendants_to_include
            Should descendant concept IDs be added to the list of concepts
            to include?
        excluded_covariate_concept_ids
            A list of concept IDs that should NOT be used to construct
            covariates.
        add_descendants_to_exclude
            Should descendant concept IDs be added to the list of concepts
            to exclude?
        included_covariate_ids
            A list of covariate IDs that should be restricted to.

        Returns
        -------
        ListVector
            An object of type ``analysisDetails``, to be used in other
            functions.

        Examples
        --------
        >>> analysisDetails <- create_analysis_details(
        ...     analysis_id = 1,
        ...     sql_file_name = "DemographicsGender.sql",
        ...     parameters = list(
        ...         analysisId = 1,
        ...         analysisName = "Gender",
        ...         domainId = "Demographics",
        ...     ),
        ...     included_covariate_concept_ids = [],
        ...     add_descendants_to_include = False,
        ...     excluded_covariate_concept_ids = [],
        ...     add_descendants_to_exclude = False,
        ...     included_covariate_ids = []
        ... )
        """
        parameters_json = json.dumps(parameters)
        return extractor_r.createAnalysisDetails(
            analysis_id,
            sql_file_name,
            parameters_json,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )

    @staticmethod
    def create_detailed_covariate_settings(analysis: list = []) -> ListVector:
        """
        Create detailed covariate settings

        creates an object specifying in detail how covariates should be
        constructed from data in the CDM model. Warning: this function is for
        advanced users only.

        Parameters
        ----------
        analysis
            An object of type ``analysisDetails``, created using
            ``create_analysis_details``.

        Returns
        -------
        ListVector
            An object of type ``covariateSettings``, to be used in other
            functions.

        Examples
        --------
        >>> analysis_details <- create_analysis_details(
        ...     analysis_id = 1,
        ...     sql_file_name = "DemographicsGender.sql",
        ...     parameters = list(
        ...         analysisId = 1,
        ...         analysisName = "Gender",
        ...         domainId = "Demographics",
        ...     ),
        ...     included_covariate_concept_ids = [],
        ...     add_descendants_to_include = False,
        ...     excluded_covariate_concept_ids = [],
        ...     add_descendants_to_exclude = False,
        ...     included_covariate_ids = []
        ... )
        >>> covSettings <- create_detailed_covariate_settings(analysis_details)
        """
        return extractor_r.createDetailedCovariateSettings(analysis)

    @staticmethod
    def create_default_temporal_covariate_settings(
        included_covariate_concept_ids: list = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list = []
    ) -> ListVector:
        """
        Create default temporal covariate settings

        creates an object specifying in detail how covariates should be
        constructed from data in the CDM model. Warning: this function is for
        advanced users only.

        Parameters
        ----------
        included_covariate_concept_ids
            A list of concept IDs that should be used to construct covariates.
        add_descendants_to_include
            Should descendant concept IDs be added to the list of concepts
            to include?
        excluded_covariate_concept_ids
            A list of concept IDs that should NOT be used to construct
            covariates.
        add_descendants_to_exclude
            Should descendant concept IDs be added to the list of concepts
            to exclude?
        included_covariate_ids
            A list of covariate IDs that should be restricted to.

        Returns
        -------
        ListVector
            An object of type ``covariateSettings``, to be used in other
            functions.

        Examples
        --------
        >>> covSettings <- create_default_temporal_covariate_settings(
        ...     included_covariate_concept_ids = [1],
        ...     add_descendants_to_include = False,
        ...     excluded_covariate_concept_ids = [2],
        ...     add_descendants_to_exclude = False,
        ...     included_covariate_ids = [1]
        ... )
        """
        return extractor_r.createDefaultTemporalCovariateSettings(
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )

    @staticmethod
    def create_detailed_temporal_covariate_settings(
        analysis: list = [],
        temporal_start_days: list[int] = range(-365, -1, 1),
        temporal_end_days: list[int] = range(-365, -1, 1)
    ):
        """
        Create detailed temporal covariate settings

        creates an object specifying in detail how temporal covariates should
        be constructed from data in the CDM model. Warning: this function is
        for advanced users only.

        Parameters
        ----------
        analysis : list, optional
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
        """
        return extractor_r.createDetailedTemporalCovariateSettings(
            analysis,
            temporal_start_days,
            temporal_end_days
        )


class DefaultTemporalCovariateSettings:

    @staticmethod
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
        temporal_start_days: list = range(-365, -1, 1),
        temporal_end_days: list = range(-365, -1, 1),
        included_covariate_concept_ids: list = [],
        add_descendants_to_include: bool = False,
        excluded_covariate_concept_ids: list = [],
        add_descendants_to_exclude: bool = False,
        included_covariate_ids: list = []
    ):
        """
        Create covariate settings

        creates an object specifying how covariates should be constructed from
        data in the CDM model.

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
            An object of type ``covariateSettings``, to be used in other
            functions.

        Examples
        --------
        >>> settings = create_temporal_covariate_settings(
        ...     use_demographics_gender=True,
        ...     use_demographics_age=True,
        ... )
        """

        temporal_start_days_list = list(temporal_start_days)
        temporal_end_days_list = list(temporal_end_days)

        return extractor_r.createTemporalCovariateSettings(
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
            temporal_start_days_list,
            temporal_end_days_list,
            included_covariate_concept_ids,
            add_descendants_to_include,
            excluded_covariate_concept_ids,
            add_descendants_to_exclude,
            included_covariate_ids
        )


class GetCovariates:

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
    ):
        """
        Get covariate information from the database

        Uses one or several covariate builder functions to construct
        covariates. This function uses the data in the CDM to construct a large
        set of covariates for the provided cohort. The cohort is assumed to be
        in an existing table with these fields: 'subject_id',
        'cohort_definition_id', 'cohort_start_date'. Optionally, an extra field
        can be added containing the unique identifier that will be used as
        rowID in the output.

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
        RS4
            Returns an object of type ``covariateData``, containing information
            on the covariates.

        Examples
        --------
        >>> covData <- get_db_covariate_data(
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

        return extractor_r.getDbCovariateData(
            connection_details, connection, oracle_temp_schema,
            cdm_database_schema, cdm_version, cohort_table,
            cohort_database_schema, cohort_table_is_temp, cohort_id,
            row_id_field, covariate_settings, aggregated
        )
