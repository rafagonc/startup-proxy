FROM python:3.6.9-stretch
ENV DEBUG="false" \
    HTTP_X_FORWARDED_PROTO="http" \
    USE_TZ="true" \
    TZ=America/Sao_Paulo \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y postgis musl-dev gcc g++ curl bash libgdal-dev libjpeg-dev
COPY requirements.txt /app/requirements.txt
RUN pip install --requirement /app/requirements.txt
COPY . /app
WORKDIR /app
USER root
EXPOSE 8080
CMD ["gunicorn", "-c", "ginit.py", "startup.wsgi"]