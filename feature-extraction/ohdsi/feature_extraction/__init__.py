import os

from rpy2 import robjects
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
    def convert_prespec_settings_to_detailed_settings():
        pass
