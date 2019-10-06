FROM python:3

RUN pip install mongoengine pytest

COPY . /app/
WORKDIR /app

ENTRYPOINT ["pytest", "-vv", "."]
