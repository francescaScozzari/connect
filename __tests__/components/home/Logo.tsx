import { expect } from '@jest/globals'
import React from 'react'

import { Logo } from '@/components/home/Logo'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<Logo title="logo" />)

describe('Logo components', () => {
  describe('<Logo />', () => {
    test('Logo svg renders correctly', () => {
      const container = setup()
      expect(container.firstChild).toMatchSnapshot()
    })
  })
})
