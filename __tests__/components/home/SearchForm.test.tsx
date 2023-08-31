import React from 'react'
import { expect } from '@jest/globals'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

import { SearchForm } from '@/components/home/SearchForm'
import { renderWithWrappers } from '@/__tests__/functions'

jest.mock('next/router', () => require('next-router-mock'))

describe('<SearchForm />', () => {
  it('SearchForm renders correctly', () => {
    const container = renderWithWrappers(<SearchForm />)
    expect(container.firstChild).toMatchSnapshot()
  })

  it('should display required error when input is empty', async () => {
    renderWithWrappers(<SearchForm />)
    fireEvent.submit(screen.getByRole('button'))
    expect(await screen.findByText('A search prompt is required')).toBeDefined()
  })

  it('should display matching error when input is too long', async () => {
    renderWithWrappers(<SearchForm />)
    fireEvent.input(screen.getByRole('textbox'), {
      target: {
        value: 'x'.repeat(2 * 1024)
      }
    })

    fireEvent.submit(screen.getByRole('button'))
    expect(await screen.findByText('Search prompt too long')).toBeDefined()
  })
})
