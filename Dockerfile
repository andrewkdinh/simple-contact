FROM tiangolo/uwsgi-nginx-flask:python3.8
LABEL maintainer="Andrew Dinh <simple-contact@andrewkdinh.com>"
LABEL version="0.1.0"

EXPOSE 8888

WORKDIR /app
ADD . .
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt