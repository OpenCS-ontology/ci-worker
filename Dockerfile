FROM python:3.10 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

WORKDIR /app
# download robot.jar - wrapper for HermiT
RUN wget https://github.com/ontodev/robot/releases/download/v1.9.1/robot.jar

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Java Temurin 17 using the official docker image
ENV JAVA_HOME=/opt/java/openjdk
COPY --from=eclipse-temurin:17 $JAVA_HOME $JAVA_HOME
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install application into container
COPY . .

ENTRYPOINT []
