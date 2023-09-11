import { expect } from '@jest/globals'
import React from 'react'

import { SearchTips } from '@/components/home/SearchTips'
import { renderWithWrappers } from '@/__tests__/functions'

const setup = () => renderWithWrappers(<SearchTips />)

describe('SearchTips components', () => {
  describe('<SearchTips />', () => {
    test('SearchTips renders correctly', () => {
      const container = setup()
      expect(container.firstChild).toMatchSnapshot()
    })
  })
})
