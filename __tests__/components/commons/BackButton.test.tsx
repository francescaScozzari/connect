import { expect } from '@jest/globals'
import React from 'react'

import { BackButton } from '@/components/commons/BackButton'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<BackButton />)

describe('Button components', () => {
  describe('<BackButton />', () => {
    test('BackButton renders correctly', () => {
      const container = setup()
      expect(container.firstChild).toMatchSnapshot()
    })
  })
})
