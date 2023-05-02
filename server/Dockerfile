FROM python:3.10

RUN apt update
RUN apt install ffmpeg -y

ENV POETRY_VERSION=1.2.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY ./app /code/app