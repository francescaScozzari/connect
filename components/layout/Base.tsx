import React from 'react'
import { ThemeProvider } from 'styled-components'
import { ToastContainer } from 'react-toastify'

import { GlobalStyle } from '@/styles/GlobalStyle'
import { Theme } from '@/models/Utils'
import { Footer } from '@/components/layout/Footer'
import themes from '@/styles/themes'

type Props = {
  children: React.ReactNode
}

const Layout = ({ children }: Props) => {
  return (
    <ThemeProvider theme={themes[Theme.light]}>
      <ToastContainer />
      <GlobalStyle />
      {children}
      <Footer />
    </ThemeProvider>
  )
}

export default Layout
