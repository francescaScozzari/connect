import React from 'react'
import { expect } from '@jest/globals'

import { Card } from '@/components/team/Card'
import { renderWithWrappers } from '@/__tests__/functions'

const authors = [
  {
    authorId: '0000-0000-0000-0001',
    documents: [
      {
        title: 'test title',
        description: 'test description'
      }
    ],
    fullName: 'Leonard Hofstadter',
    orcid: '0000-0000-0000-0001',
    university: 'Princeton University'
  }
]

const setup = () => renderWithWrappers(<Card authors={authors} />)

describe('Card component', () => {
  test('Card renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
