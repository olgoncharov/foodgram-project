FROM python:3.8.5

RUN apt update -y && \
    mkdir /code /helpers

COPY docker/create_or_update_superuser.py /helpers
COPY docker/docker-entrypoint.sh /helpers
RUN chmod +x /helpers/docker-entrypoint.sh

ENV PYTHONPATH "${PYTHONPATH}:/code/"
ENV DJANGO_SETTINGS_MODULE=conf.settings
ENV STATIC_ROOT=/code/static

WORKDIR code

COPY conf ./conf
COPY fixtures ./fixtures
COPY modules ./modules
COPY static ./static
COPY templates ./templates
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["/helpers/docker-entrypoint.sh"]
