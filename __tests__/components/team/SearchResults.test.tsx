import React from 'react'
import { expect } from '@jest/globals'

import { SearchResults } from '@/components/team/SearchResults'
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

const q = 'Exploring the Role of Microbiota in Gut-Brain Axis Communication'

const setup = () =>
  renderWithWrappers(<SearchResults authors={authors} q={q} />)

describe('Search results component', () => {
  test('All search results renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
