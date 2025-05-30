# syntax=docker/dockerfile:1

FROM node:18-bookworm-slim AS build
LABEL project="connect" service="frontend" stage="build"
ENV PATH="$PATH:./node_modules/.bin"
WORKDIR /app
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --ignore-optional --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi
COPY components ./components
COPY declarations ./declarations
COPY hooks ./hooks
COPY models ./models
COPY pages ./pages
COPY public ./public
COPY store ./store
COPY styles ./styles
COPY utils ./utils
COPY tsconfig.json next.config.js sentry.client.config.js sentry.server.config.js middleware.ts ./
ARG NEXT_PUBLIC_PLAUSIBLE_URL \
  NEXT_PUBLIC_PRIVACY_POLICY_URL \
  NEXT_PUBLIC_PROJECT_URL \
  SENTRY_AUTH_TOKEN \
  SENTRY_ORG \
  SENTRY_PROJECT_NAME \
  SENTRY_URL
ENV NEXT_TELEMETRY_DISABLED=1 \
  NODE_ENV="production" \
  PORT=3000 \
  NEXT_PUBLIC_PLAUSIBLE_URL=$NEXT_PUBLIC_PLAUSIBLE_URL \
  NEXT_PUBLIC_PRIVACY_POLICY_URL=$NEXT_PUBLIC_PRIVACY_POLICY_URL \
  NEXT_PUBLIC_PROJECT_URL=$NEXT_PUBLIC_PROJECT_URL \
  SENTRY_AUTH_TOKEN=$SENTRY_AUTH_TOKEN \
  SENTRY_ORG=$SENTRY_ORG \
  SENTRY_PROJECT_NAME=$SENTRY_PROJECT_NAME \
  SENTRY_URL=$SENTRY_URL
RUN yarn add @next/swc-linux-x64-gnu @next/swc-linux-x64-musl
RUN apt-get update \
  && apt-get install --assume-yes --no-install-recommends \
    ca-certificates \
  && yarn build \
  && unset SENTRY_AUTH_TOKEN \
  && apt-get purge --assume-yes --auto-remove \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

FROM node:18-bookworm-slim AS remote
LABEL project="connect" service="frontend" stage="remote"
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
RUN apt-get update \
  && apt-get install --only-upgrade --assume-yes \
    libc6 \
  && apt-get install --assume-yes --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*
USER nextjs
COPY ["next.config.js", "package.json", "sentry.client.config.js", "sentry.server.config.js", "server.js", "yarn.lock", "middleware.ts", "./"]
COPY ["public/", "public/"]
COPY --from=build --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=build --chown=nextjs:nodejs /app/.next/static ./.next/static
ARG SENTRY_AUTH_TOKEN \
  SENTRY_ORG \
  SENTRY_PROJECT_NAME \
  SENTRY_URL
ENV NEXT_TELEMETRY_DISABLED=1 \
  NODE_ENV="production" \
  PORT=3000 \
  SENTRY_AUTH_TOKEN=$SENTRY_AUTH_TOKEN \
  SENTRY_ORG=$SENTRY_ORG \
  SENTRY_PROJECT_NAME=$SENTRY_PROJECT_NAME \
  SENTRY_URL=$SENTRY_URL
CMD ["yarn", "start"]
