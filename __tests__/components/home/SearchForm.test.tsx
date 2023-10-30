import React from 'react'
import { expect, jest } from '@jest/globals'
import { fireEvent, screen } from '@testing-library/react'

import { SearchForm } from '@/components/home/SearchForm'
import { renderWithWrappers } from '@/__tests__/functions'

describe('<SearchForm />', () => {
  const mockHandleSubmit = jest.fn()

  it('SearchForm renders correctly', () => {
    const container = renderWithWrappers(
      <SearchForm handleSubmit={mockHandleSubmit} />
    )
    expect(container.firstChild).toMatchSnapshot()
  })

  it('submit button should be disabled when input is empty', async () => {
    renderWithWrappers(<SearchForm handleSubmit={mockHandleSubmit} />)
    expect(await screen.findByRole('submit')).toBeDisabled()
  })

  it('submit button should not be enabled when input is not empty', async () => {
    renderWithWrappers(<SearchForm handleSubmit={mockHandleSubmit} />)

    fireEvent.input(await screen.getByRole('textarea'), {
      target: {
        value: 'test'
      }
    })

    expect(await screen.findByRole('reset')).toBeVisible()
    expect(await screen.findByRole('submit')).not.toBeDisabled()
  })

  it('clear search input', async () => {
    renderWithWrappers(<SearchForm handleSubmit={mockHandleSubmit} />)

    fireEvent.input(await screen.getByRole('textarea'), {
      target: {
        value: 'test'
      }
    })

    fireEvent.click(await screen.findByRole('reset'))

    expect(await screen.findByRole('textarea')).toBeEmptyDOMElement()
  })
})
