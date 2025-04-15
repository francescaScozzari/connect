import { jest, expect } from '@jest/globals'
import React from 'react'

import Layout from '@/components/layout/Base'
import { renderWithWrappers } from '@/__tests__/functions'
import { screen, fireEvent } from '@testing-library/react'

const setup = () =>
  renderWithWrappers(
    <Layout>
      <h1>Lorem Ipsum</h1>
    </Layout>
  )

describe('Layout components', () => {
  describe('<Layout />', () => {
    test('Primary layout renders correctly', () => {
      const container = setup()
      expect(container.firstChild).toMatchSnapshot()
    })
  })
})
