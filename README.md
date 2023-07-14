# python-ohdsi
Python wrappers for (some) OHDSI tools. This project has been initiated for
supporting OMOP data sources in [vantage6](https://vantage6.ai).

Make sure you have a working R environment with the OHDSI packages installed.

# Building documentation
```bash
cd docs
make html
```

You can set the `IGNORE_R_IMPORTS` environment variable to ignore the R imports
in the documentation. This is useful when you don't have the R packages
installed but want to build the documentation anyway.

# TODO
Packages to be wrapped:
- [ ] [Capr](https://github.com/OHDSI/Capr)
- [X] [CirceR](https://github.com/OHDSI/CirceR)
- [X] [CohortGenerator](https://github.com/OHDSI/cohortgenerator)
- [X] [SqlRender](https://github.com/OHDSI/SqlRender)
- [X] [DatabaseConnector](https://github.com/OHDSI/DatabaseConnector)
- [ ] [FeatureExtraction](https://github.com/OHDSI/FeatureExtraction)
- [ ] FeatureExtractionApi (custom package to wrap FeatureExtraction module in
      a REST API)

Release packages: `ohdsi-circe`, `ohdsi-capr`, `ohdsi-cohortgenerator`, `ohdsi-sqlrender`, `ohdsi-databaseconnector`, `ohdsi-featureextraction`

# Some notes
- installing some OHDSI packages required the `--no-multiarch` flag:
  INSTALL_opts=c("--no-multiarch").
