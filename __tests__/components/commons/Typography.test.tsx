import { expect } from '@jest/globals'
import { screen } from '@testing-library/react'
import React from 'react'

import { renderWithWrappers } from '@/__tests__/functions'
import { H1, H2, H3, H4, Text } from '@/components/commons/Typography'

describe('Titles', () => {
  describe('H1', () => {
    it('Normal H1 renders correctly', () => {
      renderWithWrappers(<H1.Normal>MainTitle</H1.Normal>)
      screen.getByText('MainTitle')
    })
    it('Normal H1 renders correctly with style props', () => {
      renderWithWrappers(
        <H1.Normal uppercase italic color='red'>
          MainTitle
        </H1.Normal>
      )
      expect(screen.getByText('MainTitle')).toMatchSnapshot()
    })
    it('Big H1 renders correctly', () => {
      renderWithWrappers(<H1.Big>MainTitle</H1.Big>)
      screen.getByText('MainTitle')
    })
    it('Big H1 renders correctly with style props', () => {
      renderWithWrappers(
        <H1.Big uppercase italic color='red'>
          MainTitle
        </H1.Big>
      )
      expect(screen.getByText('MainTitle')).toMatchSnapshot()
    })
    it('Medium H1 renders correctly', () => {
      renderWithWrappers(<H1.Medium>MainTitle</H1.Medium>)
      screen.getByText('MainTitle')
    })
    it('Medium H1 renders correctly with style props', () => {
      renderWithWrappers(
        <H1.Medium uppercase italic color='red'>
          MainTitle
        </H1.Medium>
      )
      expect(screen.getByText('MainTitle')).toMatchSnapshot()
    })
  })
  describe('H2', () => {
    it('Normal H2 renders correctly', () => {
      renderWithWrappers(<H2.Normal>MainTitle</H2.Normal>)
      screen.getByText('MainTitle')
    })
    it('Normal H2 renders correctly with style props', () => {
      renderWithWrappers(
        <H2.Normal uppercase italic color='red'>
          MainTitle
        </H2.Normal>
      )
      expect(screen.getByText('MainTitle')).toMatchSnapshot()
    })
  })
  describe('H3', () => {
    it('H3 renders correctly', () => {
      renderWithWrappers(<H3.Normal>MainTitle</H3.Normal>)
      screen.getByText('MainTitle')
    })
    it('H3 renders correctly with style props', () => {
      renderWithWrappers(
        <H3.Normal uppercase italic color='red'>
          MainTitle
        </H3.Normal>
      )
      expect(screen.getByText('MainTitle')).toMatchSnapshot()
    })
  })
  describe('H4', () => {
    it('H4 renders correctly', () => {
      renderWithWrappers(<H4.Normal>MainTitle</H4.Normal>)
      screen.getByText('MainTitle')
    })
    it('H4 renders correctly with style props', () => {
      renderWithWrappers(
        <H4.Normal uppercase italic color='red'>
          MainTitle
        </H4.Normal>
      )
      expect(screen.getByText('MainTitle')).toMatchSnapshot()
    })
  })
})

describe('Text', () => {
  describe('Normal', () => {
    it('Normal Text renders correctly', () => {
      renderWithWrappers(<Text.Normal>MainParagraph</Text.Normal>)
      screen.getByText('MainParagraph')
    })
    it('Normal Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.Normal uppercase italic color='red'>
          MainParagraph
        </Text.Normal>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
    it('NormalBold Text renders correctly', () => {
      renderWithWrappers(<Text.NormalBold>MainParagraph</Text.NormalBold>)
      screen.getByText('MainParagraph')
    })
    it('NormalBold Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.NormalBold uppercase italic color='red'>
          MainParagraph
        </Text.NormalBold>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
  })
  describe('Small', () => {
    it('Small Text renders correctly', () => {
      renderWithWrappers(<Text.Small>MainParagraph</Text.Small>)
      screen.getByText('MainParagraph')
    })
    it('Small Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.Small uppercase italic color='red'>
          MainParagraph
        </Text.Small>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
    it('SmallBold Text renders correctly', () => {
      renderWithWrappers(<Text.SmallBold>MainParagraph</Text.SmallBold>)
      screen.getByText('MainParagraph')
    })
    it('SmallBold Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.SmallBold uppercase italic color='red'>
          MainParagraph
        </Text.SmallBold>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
  })
  describe('Medium', () => {
    it('Medium Text renders correctly', () => {
      renderWithWrappers(<Text.Medium>MainParagraph</Text.Medium>)
      screen.getByText('MainParagraph')
    })
    it('Medium Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.Medium uppercase italic color='red'>
          MainParagraph
        </Text.Medium>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
    it('MediumBold Text renders correctly', () => {
      renderWithWrappers(<Text.MediumBold>MainParagraph</Text.MediumBold>)
      screen.getByText('MainParagraph')
    })
    it('MediumBold Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.MediumBold uppercase italic color='red'>
          MainParagraph
        </Text.MediumBold>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
  })
  describe('Big', () => {
    it('Big Text renders correctly', () => {
      renderWithWrappers(<Text.Big>MainParagraph</Text.Big>)
      screen.getByText('MainParagraph')
    })
    it('Big Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.Big uppercase italic color='red'>
          MainParagraph
        </Text.Big>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
    it('BigBold Text renders correctly', () => {
      renderWithWrappers(<Text.BigBold>MainParagraph</Text.BigBold>)
      screen.getByText('MainParagraph')
    })
    it('BigBold Text renders correctly with style props', () => {
      renderWithWrappers(
        <Text.BigBold uppercase italic color='red'>
          MainParagraph
        </Text.BigBold>
      )
      expect(screen.getByText('MainParagraph')).toMatchSnapshot()
    })
  })
})
