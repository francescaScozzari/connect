import React from 'react'
import { expect } from '@jest/globals'
import { screen } from '@testing-library/react'

import { Card } from '@/components/team/Card'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () =>
  renderWithWrappers(
    <Card />
  )

describe('Card component', () => {
  test('Card renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
