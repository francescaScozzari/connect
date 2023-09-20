import React from 'react'
import { expect } from '@jest/globals'

import { AuthorsCounter } from '@/components/team/AuthorsCounter'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<AuthorsCounter counter={2} />)

describe('Authors counter component', () => {
  test('Counter renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
