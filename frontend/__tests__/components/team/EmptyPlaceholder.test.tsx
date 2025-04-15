import React from 'react'
import { expect } from '@jest/globals'

import { EmptyPlaceholder } from '@/components/team/EmptyPlaceholder'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<EmptyPlaceholder />)

describe('No search results placeholder component', () => {
  test('Placeholder renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
