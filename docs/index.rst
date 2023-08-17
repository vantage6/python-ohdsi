Getting started
===============

.. warning::

    Please note that this python package is not endorsed or affiliated with
    the official OHDSI community. It is a project intended for enabling
    `vantage6 <https://vantage6.ai>`_ to connect to an OMOP CDM database.

This package includes python wrappers for the following
`OHDSI libraries <https://github.com/OHDSI>`_:

* `CirceR <https://github.com/OHDSI/CirceR>`_
* `SqlRender <https://github.com/OHDSI/SqlRender>`_
* `Cohort Generator <https://github.com/OHDSI/CohortGenerator>`_
* `Database Connector <https://github.com/OHDSI/DatabaseConnector>`_
* `Feature Extraction <https://github.com/OHDSI/FeatureExtraction>`_

This packages contains, besides the python interfaces for the OHDSI libraries,
a small `RestAPI <api>`_ to interact with the libraries.

There are three use-cases to use this package:

1. Use it as a Python interface to interact with an OMOP data source.
2. Let vantage6 connect with an OMOP data source through an SQL connection
3. Let vantage6 connect through a HTTP connection with an OMOP data source


Case 1: Python OMOP interface
-----------------------------
You can use the packages to interact with the OMOP data source from your
Python environment. Note that all function are formatted in snake case
(instead of the camel-case used in the R packages). For example to execute
a simple query:

.. code:: python

    from ohdsi import database_connector

    connection_details = database_connector.create_connection_details(
        "postgresql",
        server="localhost/postgres",
        user="postgres",
        password="some-password",
        port=5432
    )
    con = database_connector.connect(connection_details)

    database_connector.execute_sql(con, "SELECT * FROM omopcdm.person LIMIT 3")


Case 2: vantage6 SQL interface
------------------------------
The vantage6 algorithm wrapper can directly connect with an OMOP instance
through a SQL connection. Important to note that the algorithm container
of vantage6  is not able to reach anything outside of its own Docker network.
It is required to setup an
`SSH Tunnel <https://docs.vantage6.ai/en/stable/technical-documentation/features/server/ssh_tunnel.html>`_
to the machine that hosts the OMOP database. An SSH tunnel brings additional
risks, therefore using the API model `vantage6-http-interface`_ is preferred.

.. uml::

    @startuml
    !theme superhero-outline

    card vantage6_node as v6 {
        rectangle node as core
        rectangle ssh_tunnel as tunnel
    }

    database OMOP
    core -right-> tunnel : SQL
    tunnel -> OMOP : SQL
    @enduml


.. _vantage6-http-interface:

Case 3: vantage6 HTTP interface
-------------------------------
The vantage6 wrapper can also use the RestAPI (included in this package) to
retrieve data from the OMOP source. Important to note that the algorithm
container of vantage6 is not able to reach anything outside of its own Docker
network. It is required to setup
`Whitelisting <https://docs.vantage6.ai/en/main/features/node/whitelisting.html>`_
to the IP/hostname and port of the machine that hosts the RestAPI.

.. uml::

    @startuml
    !theme superhero-outline

    database OMOP as OMOP

    folder python_ohdsi as API {
        interface RestAPI
        rectangle DatabaseConnector
        rectangle OHDSILibrary AS "OHDSI Library"
    }

    card vantage6_node as v6 {

        rectangle node
        rectangle whitelisting

    }

    node -> whitelisting
    whitelisting -> RestAPI : HTTP
    RestAPI -> OHDSILibrary : HTTP
    OHDSILibrary --> DatabaseConnector
    OMOP <- DatabaseConnector  : SQL
    @enduml


Table of Contents
=================

.. toctree::
   :maxdepth: 2

   self
   changelog

.. toctree::
   :maxdepth: 3
   :caption: OHDSI Python

   libraries/circe
   libraries/sql_render
   libraries/cohort_generator
   libraries/database_connector
   libraries/feature_extraction

.. toctree::
   :maxdepth: 2
   :caption: Development

   api
   contributing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
