import { createGlobalStyle } from 'styled-components'
import { normalize } from 'styled-normalize'
import 'react-toastify/dist/ReactToastify.css'

import {
  Open_Sans as OpenSans,
  Hepta_Slab as HeptaSlab,
  Poppins
} from '@next/font/google'

const baseFont = OpenSans({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  style: ['normal', 'italic']
})

const titleFont = HeptaSlab({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  style: ['normal']
})

const linkFont = Poppins({
  subsets: ['latin'],
  weight: ['400'],
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
    font-family: ${linkFont.style.fontFamily};
    font-weight: 400;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-family: ${titleFont.style.fontFamily};
  }
`
