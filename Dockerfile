FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /users-service

COPY /Pipfile.lock /Pipfile /users-service/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY . /users-service
