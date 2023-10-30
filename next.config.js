/** @type {import('next').NextConfig} */

const { withPlausibleProxy } = require('next-plausible')
const { withSentryConfig } = require('@sentry/nextjs')

const { NEXT_PUBLIC_PLAUSIBLE_URL, SENTRY_AUTH_TOKEN, SENTRY_ORG, SENTRY_PROJECT_NAME, SENTRY_URL} =
  process.env

const nextjsConfig = withPlausibleProxy()({
  compiler: { styledComponents: true },
  output: 'standalone',
  reactStrictMode: true,
  swcMinify: true,
  rewrites: async () => [
    {
      source: '/frontend/health',
      destination: '/api/health'
    },
    {
      source: '/proxy/api/event',
      destination: `${NEXT_PUBLIC_PLAUSIBLE_URL}/api/event`
    },
    {
      source: '/js/script.js',
      destination: `${NEXT_PUBLIC_PLAUSIBLE_URL}/js/script.js`
    },
  ]
})

// Sentry config. For all available options, see:
// https://github.com/getsentry/sentry-webpack-plugin#options
const SentryWebpackPluginOptions = {
  authToken: SENTRY_AUTH_TOKEN,
  org: SENTRY_ORG,
  project: SENTRY_PROJECT_NAME,
  url: SENTRY_URL
}

// Make sure adding Sentry options is the last code to run before exporting, to
// ensure that your source maps include changes from all other Webpack plugins
const config =
  SENTRY_AUTH_TOKEN && SENTRY_ORG && SENTRY_URL
    ? withSentryConfig(nextjsConfig, SentryWebpackPluginOptions)
    : nextjsConfig

module.exports = config
