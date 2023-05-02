FROM python:3.10-bullseye

RUN apt update && apt upgrade -y
RUN apt install wget ffmpeg -y
RUN apt install aptitude -y
RUN apt install wkhtmltopdf -y

ENV POETRY_VERSION=1.2.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY ./app /code/app