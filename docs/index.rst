.. python-ohdsi documentation master file, created by
   sphinx-quickstart on Wed Jul 12 08:30:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome!
========

.. warning::

    Please note that this python package is not endorsed or affiliated with
    the official ohdsi community. It is a project intended for enabling
    `vantage6 <https://vantage6.ai>`_ to connect to an OMOP CDM database.

This package includes python wrappers for the following
`OHDSI libraries <https://github.com/OHDSI>`_:

* `CirceR <https://github.com/OHDSI/CirceR>`_
* `Cohort Generator <https://github.com/OHDSI/CohortGenerator>`_
* `Database Connector <https://github.com/OHDSI/DatabaseConnector>`_
* `Feature Extraction <https://github.com/OHDSI/FeatureExtraction>`_

This package also contains a small RestAPI to interact with the Feature
Extraction module. You can use these packages to interact with an OMOP source
from Python or you use the API to retrieve record level data.

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

    from ohdsi.database_connector import Connect, Sql

    connection_details = Connect.create_connection_details(
        "postgresql",
        server="localhost/postgres",
        user="postgres",
        password="some-password",
        port=5432
    )
    con = Connect.connect(connection_details)

    Sql.execute_sql(con, "SELECT * FROM omopcdm.person LIMIT 3")


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
    !include _static/theme.puml


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

    database OMOP as OMOP

    folder python_ohdsi as API {
        interface RestAPI
        rectangle DatabaseConnector
        rectangle FeatureExtraction
    }

    card vantage6_node as v6 {

        rectangle node
        rectangle whitelisting

    }

    node -> whitelisting

    whitelisting -> RestAPI : HTTP
    RestAPI -> FeatureExtraction : HTTP
    FeatureExtraction --> DatabaseConnector
    OMOP <- DatabaseConnector  : SQL

    @enduml


Table of Contents
=================

.. toctree::
   :maxdepth: 3

   self
   circe
   sql_render
   database_connector
   cohort_generator
   feature_extraction


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
