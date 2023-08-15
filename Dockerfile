FROM python:3.11-bullseye

# set dockerfile var
ENV PORT=8000

# install compiler
RUN apt-get update && apt-get install -y build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev
RUN apt-get install -y dirmngr apt-transport-https ca-certificates software-properties-common gnupg2

# install Java
RUN apt-get install -y openjdk-17-jre
RUN apt-get install -y openjdk-17-jdk


# install R
# ENV R_BASE_VERSION=4.3.1
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'
RUN add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian bullseye-cran40/'
RUN apt-get update
RUN apt-get install -y r-base

RUN R CMD javareconf

# RUN R -e "install.packages('devtools', repos='http://cran.us.r-project.org')"
RUN Rscript -e "install.packages('DatabaseConnector')"
RUN Rscript -e "install.packages('drat')"
RUN Rscript -e "drat::addRepo('OHDSI'); install.packages('FeatureExtraction')"


COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
# port where the API is liste
EXPOSE ${PORT}

ENV LD_LIBRARY_PATH=/usr/lib/jvm/java-17-openjdk-amd64/lib/server/

RUN pip install psycopg2-binary
# start the flask app
# CMD uwsgi --http 0.0.0.0:${PORT} --master -p 4 -w run:app
CMD gunicorn -b 0.0.0.0 -w 1 'api.src:app'

# /usr/local/lib/python3.11/site-packages/ohdsi/database_connector