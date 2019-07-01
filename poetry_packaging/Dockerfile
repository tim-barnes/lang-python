# -- Base Image --
# Installs application dependencies
FROM python:3.7.2 as base
ENV PYTHONUNBUFFERED 1
# Install dependecy manager
RUN pip install poetry>=0.12 \
 && poetry config settings.virtualenvs.create false
# Set up application environment
WORKDIR /app
# COPY ./src/pyproject.toml ./src/poetry.lock ./
COPY ./src .
RUN poetry install --no-dev --no-interaction && rm -rf pip-wheel-metadata/

# -- Test Image --
# Code to be mounted into /app
FROM base as test
RUN poetry install --no-interaction
ENTRYPOINT ["pytest", "-vv"]

# -- Production Image --
# Runs the service
FROM base as prod
ARG PYPI_REPO
COPY ./src .

# Build the distribution ready for deployment
RUN poetry config repositories.tracr $PYPI_REPO && \
    poetry config --list && \
    poetry build
ENTRYPOINT [ "poetry", "publish", "-r", "tracr" ]
