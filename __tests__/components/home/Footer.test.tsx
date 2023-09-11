import { expect } from '@jest/globals'

import React from 'react'

import { Footer } from '@/components/home/Footer'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<Footer />)

describe('Footer components', () => {
  describe('<Footer />', () => {
    test('Footer renders correctly', () => {
      const container = setup()
      expect(container.firstChild).toMatchSnapshot()
    })
  })
})
