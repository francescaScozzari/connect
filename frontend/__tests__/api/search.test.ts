import { searchAuthors } from '@/utils/api/search'
import { expect } from '@jest/globals'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

describe('Search API Requests', () => {
  const mock = new MockAdapter(axios)

  it('Should retrieve authors data successfully', () => {
    mock.onGet('/api/author/search/?team_size=1&q=test').reply(200, {
      fullName: 'Leonard Hofstadter',
      orcid: '0000-0000-0000-0001',
      university: 'Princeton University'
    })
    searchAuthors({}, { teamSize: 1, prompt: 'test' }).then(({ data }) => {
      expect(data).toMatchObject({
        fullName: 'Leonard Hofstadter',
        orcid: '0000-0000-0000-0001',
        university: 'Princeton University'
      })
    })
  })
})
