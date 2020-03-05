FROM python:3.7.6
MAINTAINER masterarrow "masterarrows@gmail.com"
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev python3-dev
RUN mkdir -p /var/log/gunicorn
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
