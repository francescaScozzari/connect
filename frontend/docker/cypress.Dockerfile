# syntax=docker/dockerfile:1

FROM cypress/base:18.16.1
LABEL project="connect" service="frontend" stage="e2e"
ARG USER=appuser
ENV APPUSER=$USER \
  CYPRESS_CACHE_FOLDER="/home/$USER/.cache/Cypress" \
  PATH="$PATH:./node_modules/.bin"
WORKDIR /app
RUN useradd --skel /dev/null --create-home $APPUSER
RUN chown $APPUSER:$APPUSER /app
USER $APPUSER
COPY --chown=$APPUSER \
    ./package.json \
    ./scripts/entrypoint.sh \
    ./scripts/ci_e2e.sh \
    ./tsconfig.json \
    ./
RUN yarn add cypress typescript
RUN cypress install
RUN mkdir cypress-outputs
ENTRYPOINT [ "./entrypoint.sh" ]
CMD [ "./ci_e2e.sh" ]
