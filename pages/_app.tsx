import { Provider } from 'react-redux'
import Head from 'next/head'
import React from 'react'
import PlausibleProvider from 'next-plausible'
import store from '@/store'

import Layout from '@/components/layout/Base'

import type { AppProps } from 'next/app'

function MyApp({ Component, pageProps }: AppProps) {
  const title = 'Connect'

  const domain =
    process.env.NODE_ENV === 'production' && process.env.NEXT_PUBLIC_PROJECT_URL
      ? new URL(process.env.NEXT_PUBLIC_PROJECT_URL).hostname
      : 'localhost'

  const customDomain =
    process.env.NODE_ENV === 'production' &&
    process.env.NEXT_PUBLIC_PLAUSIBLE_URL
      ? process.env.NEXT_PUBLIC_PLAUSIBLE_URL
      : 'https://plausible.io'

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <PlausibleProvider
        domain={domain}
        customDomain={customDomain}
        selfHosted
      >
        <Provider store={store}>
          <Layout>
            <Component {...pageProps} />
          </Layout>
        </Provider>
      </PlausibleProvider>
    </>
  )
}

export default MyApp
