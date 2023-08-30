FROM python:3.11-slim-bookworm AS base

LABEL project="connect" service="backend" stage="base"
ARG DEBIAN_FRONTEND=noninteractive
ARG USER=appuser
ENV APPUSER=$USER LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 WORKDIR=/app
WORKDIR $WORKDIR
RUN useradd --skel /dev/null --create-home $APPUSER
RUN chown $APPUSER:$APPUSER $WORKDIR
ENV PATH="/home/${APPUSER}/.local/bin:${PATH}"
ARG PACKAGES_PATH=/home/${APPUSER}/.local/lib/python3.11/site-packages
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        curl \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/base.txt requirements/base.txt
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
    && su $APPUSER -c "python3 -m pip install --user --no-cache-dir -r requirements/base.txt" \
    && find ${PACKAGES_PATH} -regex '^.*/locale/.*/*.\(mo\|po\)$' -not -path '*/en*' -not -path '*/it*' -delete || true \
    && apt-get purge --assume-yes --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/common.txt requirements/common.txt
RUN su $APPUSER -c "python3 -m pip install --user --no-cache-dir -r requirements/common.txt" \
    && find ${PACKAGES_PATH} -regex '^.*/locale/.*/*.\(mo\|po\)$' -not -path '*/en*' -not -path '*/it*' -delete || true

FROM base AS test

LABEL project="connect" service="backend" stage="test"
ENV DJANGO_CONFIGURATION=Testing
USER $APPUSER
COPY --chown=$APPUSER ./requirements/test.txt requirements/test.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/test.txt
COPY --chown=$APPUSER . .
ENTRYPOINT ["./scripts/entrypoint_test.sh"]
CMD ./scripts/test.sh

FROM base AS remote

LABEL project="connect" service="backend" stage="remote"
ENV DJANGO_CONFIGURATION=Remote INTERNAL_SERVICE_PORT=8000
USER $APPUSER
ARG PACKAGES_PATH=/home/${APPUSER}/.local/lib/python3.11/site-packages
COPY --chown=$APPUSER ./requirements/remote.txt requirements/remote.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/remote.txt
COPY --chown=$APPUSER . .
RUN DJANGO_SECRET_KEY=build python3 -m manage collectstatic --clear --link --noinput
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["python3", "-m", "gunicorn", "connect.asgi"]

FROM base AS local

LABEL project="connect" service="backend" stage="local"
ENV DJANGO_CONFIGURATION=Local INTERNAL_SERVICE_PORT=8000
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gcc \
        gettext \
        git \
        graphviz \
        libpq-dev \
        make \
        openssh-client \
        postgresql-client
USER $APPUSER
COPY --chown=$APPUSER ./requirements/local.txt requirements/local.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/local.txt
COPY --chown=$APPUSER . .
RUN DJANGO_SECRET_KEY=build python3 -m manage collectstatic --clear --link --noinput
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD python3 -m manage runserver 0.0.0.0:${INTERNAL_SERVICE_PORT}
