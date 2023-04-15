FROM python:3.10-slim-buster

WORKDIR /usr/src/app

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

# install psycogy dependencies
RUN apt-get update --fix-missing
RUN apt-get install -y build-essential libpq-dev
RUN rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip pipenv flake8

COPY Pipfile* ./
RUN pipenv install  --ignore-pipfile

COPY . .

# lint
RUN flake8 --ignore=E501,F401 .