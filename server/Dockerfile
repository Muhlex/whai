FROM python:3.10-bullseye

RUN apt update && apt upgrade -y
RUN apt install wget ffmpeg -y
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
RUN apt install -f ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb

ENV POETRY_VERSION=1.2.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY ./app /code/app