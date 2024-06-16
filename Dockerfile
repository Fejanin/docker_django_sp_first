FROM python:3.10-alpine3.19

COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip3 install -r /temp/requirements.txt
RUN adduser --disabled-password service-user

USER service-user
