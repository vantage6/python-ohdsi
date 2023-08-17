Circe
=====

The section bellow is adjusted from the
`Circe <https://github.com/OHDSI/CirceR>`_ docs.

Introduction
------------
A python-wrapper for `Circe <https://www.github.com/OHDSI/circe-be>`_, a
library for creating queries for the OMOP Common Data Model. These queries
are used in cohort definitions (CohortExpression) as well as custom features
(CriteriaFeature). This package provides convenient wrappers for Circe
functions, and includes the necessary Java dependencies.

Features
--------
* Convert a JSON cohort expression into a markdown print-friendly presentation.
* Convert a JSON cohort expression into SQL.

Installation
------------
Install the python wrapper with pip:

.. code-block:: bash

    pip install ohdsi-circe

Since this package only wraps the CirceR both Java and R are required.
Full instructions on how to configure your R and Java environment can be found
in the OHDSI documentation:
`Setting up the R environment <https://ohdsi.github.io/Hades/rSetup.html>`_.

On debian-based systems, install the dependencies boils down to:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install r-base openjdk-17-jdk openjdk-17-jre

.. code-block:: R

    install.packages("remotes")
    remotes::install_github("OHDSI/CirceR")




Function Reference
------------------
.. automodule:: ohdsi.circe
    :members:
    :undoc-members:
    :show-inheritance: