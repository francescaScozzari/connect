import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL,
    setupNodeEvents(on, config) {
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      return require('./cypress/plugins/index.ts')(on, config)
    }
  },
  env: {
    'privacyPolicyUrl': process.env.NEXT_PUBLIC_PRIVACY_POLICY_URL
  },
  screenshotsFolder: 'cypress-outputs',
  video: false,
  viewportHeight: 720,
  viewportWidth: 1280
})
