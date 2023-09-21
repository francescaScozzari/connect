import React from 'react'
import { styled } from 'styled-components'

import { Text } from '@/components/commons/Typography'
import { Author } from '@/models/Authors'
import { Card } from './Card'
import { AuthorsCounter } from './AuthorsCounter'

type Props = {
  authors: Author[]
  q: string
}

const SearchResults = ({ authors, q }: Props) => {
  return (
    <MainSection>
      <Sidebar>
        <AuthorsCounter counter={authors.length} />
        <Paragraph>
          <Title>
            Why we’re suggesting these researches for your research project
          </Title>
          <br />"{q}"
        </Paragraph>
      </Sidebar>
      <CardsContainer>
        <Card authors={authors} />
      </CardsContainer>
    </MainSection>
  )
}

const Title = styled.span`
  display: inline-block;
  color: ${({ theme }) => theme.colors.primary[0]};
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.5;
`

const Paragraph = styled(Text.Normal)`
  font-size: 1.125rem;
  line-height: 2.25;
  color: #242424;
  height: fit-content;
  max-height: 60vh;
  text-align: start;
  padding: 2em;
  overflow: scroll;
  background-color: white;
  border-radius: 1.25em;
  border: 1px solid #c9d2ec;
`

const MainSection = styled.section`
  width: 100%;
  padding: 4em;
  display: grid;
  column-gap: 3em;
  grid-template-columns: 0.5fr 1fr;
  grid-auto-flow: column;
  background-color: ${({ theme }) => theme.colors.primary[0]};
`

const Sidebar = styled.div`
  grid-column: 1;
  display: flex;
  flex-direction: column;
  height: fit-content;
  gap: 1em;
  position: sticky;
  top: 2em;
`

const CardsContainer = styled.div`
  grid-column: 2;
  display: flex;
  flex-direction: column;
  gap: 1em;
  width: 100%;
`

export { SearchResults }
