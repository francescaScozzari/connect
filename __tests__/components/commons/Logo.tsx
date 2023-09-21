import { expect } from '@jest/globals'
import React from 'react'

import { BigLogo, SmallLogo } from '@/components/commons/Logo'
import { renderWithWrappers } from '@/__tests__/functions'

describe('Logo components', () => {
  test('BigLogo renders correctly', () => {
    const setup = () => renderWithWrappers(<BigLogo title="big logo" />)
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })

  test('SmallLogo renders correctly', () => {
    const setup = () => renderWithWrappers(<SmallLogo title="small logo" />)
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
