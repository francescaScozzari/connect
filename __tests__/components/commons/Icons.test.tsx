import React from 'react'
import { expect } from '@jest/globals'
import { screen } from '@testing-library/react'

import { IconArrowCircle } from '@/components/commons/Icons'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<IconArrowCircle title="Arrow circle" />)

describe('Icons', () => {
  test('IconArrowCircle renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
    screen.getByTitle('Arrow circle')
  })
})
