import { ThemeProvider } from 'styled-components'
import React from 'react'

import { GlobalStyle } from '@/styles/GlobalStyle'
import { Theme } from '@/models/Utils'
import themes from '@/styles/themes'

type Props = {
  children: React.ReactNode
}

const Layout = ({ children }: Props) => {
  return (
    <ThemeProvider theme={themes[Theme.light]}>
      <GlobalStyle />
      {children}
    </ThemeProvider>
  )
}

export default Layout
