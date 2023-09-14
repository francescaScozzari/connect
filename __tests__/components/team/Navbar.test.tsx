import React from 'react'
import { expect } from '@jest/globals'
import { screen } from '@testing-library/react'

import { Navbar } from '@/components/team/Navbar'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<Navbar />)

describe('Navbar component', () => {
  test('Navbar renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
