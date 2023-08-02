API
===

.. uml::

    @startuml
    !theme superhero-outline

    left to right direction

    node data_station AS "Data Station" {
        rectangle data AS "Data VM" {
            database jobs
            package python_ohdsi AS "Python-OHDSI" {
                rectangle DatabaseConnector
                rectangle CohortGenerator
                rectangle FeatureExtraction
                rectangle Circe
                rectangle other AS "..."
                rectangle API
            }
            collections pickles
            database omop
        }
        rectangle v6 AS "vantage6-node VM" {
            rectangle algorithm
        }

    }


    omop <-- DatabaseConnector

    DatabaseConnector <-- CohortGenerator
    DatabaseConnector <-- FeatureExtraction
    DatabaseConnector <-- Circe
    DatabaseConnector <-- other

    API <-- algorithm : http

    API -u-> jobs
    API -> pickles

    CohortGenerator <-- API
    FeatureExtraction <-- API
    Circe <-- API
    other <-- API

    @enduml


.. toctree::
   :maxdepth: 3

   self
