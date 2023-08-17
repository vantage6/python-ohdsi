API
====
The API allows applications to retrieve data from an OMOP source through
a http interface. The API is implemented in Python and uses the Flask
framework.

Because OMOP queries can be quite time consuming, therefore the API will make
use of background tasks. The API will return a job id, which can be used to
retrieve the results of the query later.

.. uml::

    @startuml
    !theme superhero-outline

    left to right direction

    card data AS "Data VM" {
        database jobs
        package python_ohdsi AS "Python-OHDSI" {
            rectangle DatabaseConnector
            rectangle OHDSI_Library AS "OHDSI Library"
            rectangle API
        }
        database omop
    }
    card v6 AS "vantage6-node VM" {
        rectangle algorithm
    }

    omop <-- DatabaseConnector
    DatabaseConnector <- OHDSI_Library

    API <-- algorithm : http
    API -> jobs

    OHDSI_Library <-- API

    @enduml


Start the API
-------------

.. code:: yaml

    docker compose up -d

Or to run it in development mode:

.. code:: yaml

    docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

Build the API
-------------

.. code:: yaml

    docker compose build
