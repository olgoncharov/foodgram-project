FROM python:3.8.5-alpine3.12

RUN apt update -y && \
    mkdir /code /helpers

COPY build/django_create_superuser.py /helpers
COPY build/docker-entrypoint.sh /helpers
RUN chmod +x /helpers/docker-entrypoint.sh

ENV PYTHONPATH "${PYTHONPATH}:/code/"
ENV DJANGO_SETTINGS_MODULE=conf.settings

WORKDIR code

COPY conf ./conf
COPY fixtures ./fixtures
COPY modules ./modules
COPY statis ./static
COPY templates ./templates
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["/helpers/docker-entrypoint.sh"]
