FROM python:3.8.5

RUN apt update -y && \
    mkdir /code

COPY docker/entrypoint.py /code
COPY docker/docker-entrypoint.sh /code
RUN chmod +x /code/docker-entrypoint.sh

ENV PYTHONPATH "${PYTHONPATH}:/code/"
ENV DJANGO_SETTINGS_MODULE=conf.settings

WORKDIR code

COPY conf ./conf
COPY fixtures ./fixtures
COPY modules ./modules
COPY static ./static
COPY templates ./templates
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["/code/docker-entrypoint.sh"]
