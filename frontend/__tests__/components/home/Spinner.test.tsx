import { expect } from '@jest/globals'
import React from 'react'

import { Spinner } from '@/components/home/Spinner'
import { renderWithWrappers } from '@/__tests__/functions'
import { screen } from '@testing-library/react'

describe('<Spinner />', () => {
  test('Spinner is visible', async () => {
    renderWithWrappers(<Spinner spinnerLoading={true} />)
    expect(await screen.findByText(/we are searching/i)).toBeVisible()
  })
})
