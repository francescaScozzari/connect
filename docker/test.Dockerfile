# syntax=docker/dockerfile:1

FROM node:18-bookworm-slim
LABEL company="20tab" project="connect" service="frontend" stage="test"
ARG DEBIAN_FRONTEND=noninteractive GROUP_ID=1001 USER=appuser
ENV APPUSER=$USER \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    NEXT_TELEMETRY_DISABLED=1 \
    NODE_ENV="development" \
    PATH="$PATH:./node_modules/.bin" \
    TZ='Europe/Rome' \
    WORKDIR=/app \
    HOME=/app
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        g++ \
        make \
        python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR $WORKDIR
RUN addgroup --system --gid $GROUP_ID $APPUSER
RUN adduser --system --uid $GROUP_ID $APPUSER
RUN chown $GROUP_ID:$APPUSER $WORKDIR
USER $GROUP_ID:$USER_ID
COPY --chown=$APPUSER \
    ./scripts/entrypoint_test.sh \
    ./scripts/test.sh \
    .eslintrc.json \
    .prettierrc.json \
    jest.config.js \
    middleware.ts \
    next.config.js \
    package.json \
    tsconfig.json \
    yarn.lock \
    ./
RUN yarn config set cache-folder $HOME/.yarn-cache
ENTRYPOINT ["./entrypoint_test.sh"]
CMD ["./test.sh"]
