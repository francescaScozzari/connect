import { expect } from '@jest/globals'
import React from 'react'

import { Button } from '@/components/commons/Button'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () =>
  renderWithWrappers(<Button />)

describe('Button components', () => {
  describe('<Button />', () => {
    test('Button primary ui renders correctly', () => {
      const container = setup()
      expect(container.firstChild).toMatchSnapshot()
    })
  })
})
