import React from 'react'
import { expect } from '@jest/globals'

import { SearchResults } from '@/components/team/SearchResults'
import { renderWithWrappers } from '@/__tests__/functions'

const authors = [
  {
    authorId: '0000-0000-0000-0001',
    documents: [
      {
        description: 'test description',
        doi: '99.9999/999-9-999-99999-2_22',
        highlights: ['test'],
        score: 0.2,
        title: 'test title'
      }
    ],
    fullName: 'Leonard Hofstadter',
    orcid: '0000-0000-0000-0001',
    score: 0.5,
    university: 'Princeton University'
  }
]

const givenSentence = {
  text: 'Exploring the Role of Microbiota in Gut-Brain Axis Communication',
  highlights: ['test', 'communication']
}

const setup = () =>
  renderWithWrappers(
    <SearchResults authors={authors} givenSentence={givenSentence} />
  )

describe('Search results component', () => {
  test('All search results renders correctly', () => {
    const container = setup()
    expect(container.firstChild).toMatchSnapshot()
  })
})
