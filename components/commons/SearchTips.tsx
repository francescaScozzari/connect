import React from 'react'
import { styled } from 'styled-components'

import { Text } from '@/components/commons/Typography'
import { IconNote, IconTarget } from './Icons'

type Props = {
  titleColor?: string
  textColor?: string
}

const SearchTips = ({
  titleColor = '#2B2D42',
  textColor = '#242424'
}: Props) => {
  return (
    <Wrapper>
      <SubWrapper>
        <IconNote title={'note'} color={titleColor} />
        <Paragraph color={textColor}>
          <Title color={titleColor}>Start from the research call</Title>
          <br /> If you are working or will have to work on a research paper for
          a call, you might report in the search field the title or objectives
          of that
        </Paragraph>
      </SubWrapper>

      <SubWrapper>
        <IconTarget title={'target'} color={titleColor} />
        <Paragraph color={textColor}>
          <Title color={titleColor}>More detail for greater match</Title>
          <br /> Enter as much information, don't limit yourself to a single
          word, that way we can narrow it down and suggest the researchers best
          suited to your need
        </Paragraph>
      </SubWrapper>
    </Wrapper>
  )
}

const Wrapper = styled.div`
  display: flex;
  gap: 2em;
  max-width: 67em;
  margin: 4em 0;

  @media (max-width: 1280px) {
    max-width: 46em;
  }

  @media (max-width: 768px) {
    max-width: 37.5em;
  }
`

const SubWrapper = styled.div`
  display: flex;
  gap: 0.5em;
  padding: 1.5em;
  align-items: start;
  max-width: 29.85em;
  border: 1px solid #7a83ab;
  border-radius: 1.25em;

  svg {
    flex-shrink: 0;
  }
`

const Paragraph = styled(Text.Normal)<{ color: string }>`
  line-height: 1.5;
  color: ${({ color }) => color};
`

const Title = styled.span<{ color: string }>`
  display: inline-block;
  color: ${({ color }) => color};
  margin-bottom: 0.5em;
  font-weight: 600;
  line-height: 1.5;
`

export { SearchTips }
