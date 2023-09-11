import React from 'react'
import { styled } from 'styled-components'

import { Text } from '@/components/commons/Typography'
import { IconCopy, IconTarget } from '../commons/Icons'

const SearchTips = () => {
  return (
    <OuterWrapper>
      <Text.NormalBold>
        Search tips to get the best research team suggestion
      </Text.NormalBold>
      <InnerWrapper>
        <SubWrapper>
          <IconCopy title={'paper'} />
          <Text.Normal>
            <Highlight>Start from the the research call</Highlight>
            <br /> If you are working or will have to work on a research paper
            for a call, you might report in the search field the title or
            objectives of that
          </Text.Normal>
        </SubWrapper>

        <SubWrapper>
          <IconTarget title={'target'} />
          <Text.Normal>
            <Highlight>More detail for greater match</Highlight>
            <br /> Enter as much information, don't limit yourself to a single
            word, that way we can narrow it down and suggest the researchers
            best suited to your need
          </Text.Normal>
        </SubWrapper>
      </InnerWrapper>
    </OuterWrapper>
  )
}

const OuterWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2em;
  max-width: 53em;
  background-color: #f5f5f5;
  padding: 4em 2em;

  p {
    align-self: center;
  }

  @media (max-width: 1280px) {
    max-width: 46em;
  }

  @media (max-width: 768px) {
    max-width: 37.5em;
  }
`
const InnerWrapper = styled.div`
  display: flex;
  gap: 2em;
`
const SubWrapper = styled.div`
  display: flex;
  gap: 0.5em;
  align-items: start;

  svg {
    flex-shrink: 0;
  }
`
const Highlight = styled.span`
  display: inline;
  font-size: ${({ theme }) => theme.texts.normalBold.fontSize};
  font-weight: ${({ theme }) => theme.texts.normalBold.fontWeight};
`

export { SearchTips }
