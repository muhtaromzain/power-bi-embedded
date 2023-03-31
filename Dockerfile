FROM python:3.10.7-slim-bullseye
RUN adduser --disabled-password --gecos '' power_bi_service
WORKDIR /home/power_bi_service
RUN set -eux; \
         apt-get update; \
         DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         libffi-dev;
COPY requirements.txt /
COPY app app/
COPY gunicorn.sh ./
RUN chown -R power_bi_service:power_bi_service ./
RUN pip3 install -r /requirements.txt
USER power_bi_service
ENV PYTHONPATH "${PYTHONPATH}:/home/power_bi_service/"

ENTRYPOINT ["./gunicorn.sh"]