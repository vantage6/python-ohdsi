# python-ohdsi
[![PyPI Circe](https://badge.fury.io/py/ohdsi-circe.svg)](https://badge.fury.io/py/ohdsi-circe)
[![PyPI DatabaseConnector](https://badge.fury.io/py/ohdsi-database-connector.svg)](https://badge.fury.io/py/ohdsi-database-connector)
[![PyPI FeatureExtraction](https://badge.fury.io/py/ohdsi-feature-extraction.svg)](https://badge.fury.io/py/ohdsi-feature-extraction)
[![PyPI SQLRender](https://badge.fury.io/py/ohdsi-sqlrender.svg)](https://badge.fury.io/py/ohdsi-sqlrender)

Python wrappers for (some) OHDSI tools. This project has been initiated for
supporting OMOP data sources in [vantage6](https://vantage6.ai).

Make sure you have a working R environment with the OHDSI packages installed.

## Installation

### Python binding
Interact with the OMOP database using a python interface.

* Install Java JDK.
* Install R: `sudo apt-get install r-base` (set `R_HOME`)
* Install R packages

```bash
pip install python-ohdsi
```

### API service
Spin up a small webserver next to the OMOP database to allow HTTP requests to
the OMOP database. You can use the prebuild image from dockerhub:

```bash
docker pull ...
docker run ...
```

Or you can build the image yourself:

```bash
docker build -t ohdsi-api .
docker run -p 5000:5000 ohdsi-api
```

Or you can run the API service directly from the source code:

```bash
pip install -r requirements.txt
python api.py
```

## Building documentation
```bash
cd docs
export IGNORE_R_IMPORTS=True
make html
```

```powershell
cd docs
Set-Item -Path Env:IGNORE_R_IMPORTS -Value True
make html
```

or you can use ``make livehtml`` to automatically rebuild the documentation
when a file is changed.

You can set the `IGNORE_R_IMPORTS` environment variable to ignore the R imports
in the documentation. This is useful when you don't have the R packages
installed but want to build the documentation anyway.

## User Documentation
The user documentation can be found at [readthedocs](https://python-ohdsi.readthedocs.io/en/latest/).
