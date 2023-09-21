import { jest, expect } from '@jest/globals'
import React from 'react'

import { Footer } from '@/components/layout/Footer'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<Footer />)

describe('<Footer />', () => {
  test('Footer renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
