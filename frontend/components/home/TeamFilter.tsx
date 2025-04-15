import React from 'react'
import styled from 'styled-components'
import { IconGroup } from '../commons/Icons'
import { Text } from '../commons/Typography'

export const TeamFilter = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <InnerWrapper>
        <IconGroup title="team" fill="#c9d2ec" />
        <DescriptionWrapper>
          <Text.NormalBold color="#c9d2ec">N. Researchers</Text.NormalBold>
          <Text.Small color="white">Min 5 / Max 20</Text.Small>
        </DescriptionWrapper>
        <FilterWrapper>{children}</FilterWrapper>
      </InnerWrapper>
    </>
  )
}

const InnerWrapper = styled.div`
  position: relative;
  margin-bottom: 1em;
  display: flex;
  gap: 0.75em;
`

const DescriptionWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 0.25em;
`

const FilterWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 7.75em;
  background-color: white;
  border: 4px solid #e5e5e5;
  border-radius: 3.75em;
`
