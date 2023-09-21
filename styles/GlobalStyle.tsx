import { createGlobalStyle } from 'styled-components'
import { normalize } from 'styled-normalize'
import 'react-toastify/dist/ReactToastify.css'

import { Open_Sans as OpenSans, Poppins, Roboto } from '@next/font/google'

const baseFont = Poppins({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  style: ['normal', 'italic']
})

const secondaryFont = OpenSans({
  subsets: ['latin'],
  weight: ['400', '700'],
  style: ['normal']
})

const tertiaryFont = Roboto({
  subsets: ['latin'],
  weight: ['900'],
  style: ['normal']
})

export const GlobalStyle = createGlobalStyle`
  ${normalize}

  :root {
    font-size: 1em;
  }

  * {
    box-sizing: border-box;
  }

  body {
    font-family: ${baseFont.style.fontFamily};
    font-weight: 400;
    background-color: ${({ theme }) => theme.colors.neutrals[0]};
    color: ${({ theme }) => theme.colors.ui8};
  }

  a {
    text-decoration: none;
  }

  span {
    font-family: ${baseFont.style.fontFamily};
    font-weight: 400;
  }

  p {
    font-family: ${secondaryFont.style.fontFamily};
    font-weight: 400;
  }

  strong {
    font-family: ${tertiaryFont.style.fontFamily};
    font-weight: 900;
  }

  mark {
    background-color: #e8f5fb;
    padding: 4px 2px;
    text-decoration-skip-ink: none;
    text-decoration: underline #1B9BD9 4px;
    text-underline-position: under;
  }


`
