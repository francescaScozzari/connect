import type { DefaultTheme } from 'styled-components'

const theme: DefaultTheme = {
  colors: {
    ui1: '#F1F9FF',
    ui2: '#EDF8FF',
    ui3: '#E0EAEF',
    ui4: '#E5E8EB',
    ui5: '#A6B0BB',
    ui6: '#696D73',
    ui7: '#333333',
    ui8: '#1C1C1C',
    link: '#316CF4',
    activeLink: '#007AFF',
    successLabel: '#B0FFD9',
    errorLabel: '#FFD0D0',
    primary: {
      0: '#2B2D42'
    },
    secondary: {
      0: '#CE2F7C'
    },
    status: {
      info: '#007AFF',
      attention: '#FFC700',
      success: '#1AC755',
      warning: '#FF7A00',
      error: ''
    },
    neutrals: {
      0: '#FFFFFF',
      100: '#F4F7F8',
      200: '#D2D7DA',
      300: '#B3B9BD',
      400: '#949CA1',
      500: '#777F86',
      600: '#404952'
    }
  },
  titles: {
    h1: {
      normal: {
        fontSize: '35px',
        fontWeight: 700
      },
      big: {
        fontSize: '50px',
        fontWeight: 700
      },
      medium: {
        fontSize: '49px',
        fontWeight: 700
      }
    },
    h2: {
      normal: {
        fontSize: '32px',
        fontWeight: 700
      }
    },
    h3: {
      normal: {
        fontSize: '24px',
        fontWeight: 700
      }
    },
    h4: {
      normal: {
        fontSize: '20px',
        fontWeight: 700
      }
    }
  },
  texts: {
    normal: {
      fontSize: '16px',
      fontWeight: 400
    },
    normalBold: {
      fontSize: '16px',
      fontWeight: 700
    },
    big: {
      fontSize: '18px',
      fontWeight: 400
    },
    bigBold: {
      fontSize: '18px',
      fontWeight: 700
    },
    medium: {
      fontSize: '14px',
      fontWeight: 400
    },
    mediumBold: {
      fontSize: '14px',
      fontWeight: 600
    },
    small: {
      fontSize: '12px',
      fontWeight: 400
    },
    smallBold: {
      fontSize: '12px',
      fontWeight: 500
    }
  }
}

export { theme }
