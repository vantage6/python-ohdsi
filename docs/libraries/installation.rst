Installation
============

In order to use the python binding to the OHDSI libraries you need to have:

* Java 1.8+ installed
* R environment
* R OHDSI libraries installed


```R
# DatabaseConnector
install.packages('DatabaseConnector')

# FeatureExtraction
install.packages('drat')
drat::addRepo('OHDSI'); install.packages('FeatureExtraction')
```