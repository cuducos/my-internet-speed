FROM python:3.6.8-slim

WORKDIR /code
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock

# +-------------+-------------+
# | Package     | Required by |
# +-------------|-------------+
# | gcc         | psycopg2    |
# | libpq-dev   | psycopg2    |
# | python3-dev | psycopg2    |
# +-------------+-------------+
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get -qq -y install apt-transport-https && \
    apt-get -qq -y install gcc libpq-dev python3-dev && \
    pip install -U pip && \
    pip install -U black pipenv && \
    pipenv install --dev --deploy --system && \
    apt-get -qq -y remove apt-transport-https gcc python3-dev && \
    apt-get -qq -y autoremove && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

ADD my_internet_speed/ my_internet_speed/
CMD ["celery", "-A", "my_internet_speed", "worker", "-B"]
