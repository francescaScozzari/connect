import React from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { H3, Text } from '@/components/commons/Typography'
import { Navbar } from '@/components/team/Navbar'
import { useAppSelector } from '@/store'
import { Card } from '@/components/team/Card'

const Team: NextPage = () => {
  const { authors, q } = useAppSelector(state => state.search)

  return (
    <>
      <Navbar />
      <Container>
        <TitleSection>
          <H3.Normal>Your research team</H3.Normal>
        </TitleSection>
        <MainSection>
          <Sidebar>
            <Text.NormalBold>
              Why we’re suggesting these researches for your research project
            </Text.NormalBold>
            <Text.Normal>{q.length ? q : '-'}</Text.Normal>
          </Sidebar>
          <CardsContainer>
            <Label>
              <Bold as="span">{authors?.length ?? '0'}</Bold> researchers
              identified
            </Label>
            <Card authors={authors} />
          </CardsContainer>
        </MainSection>
      </Container>
    </>
  )
}

const MainSection = styled.section`
  width: 100%;
  padding: 2.5em;
  display: grid;
  column-gap: 3em;
  grid-template-columns: 0.5fr 0.8fr;
  grid-auto-flow: column;
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

const Label = styled(Text.Normal)`
  font-size: 0.8125em;
`

const Bold = styled(Label)`
  font-weight: bold;
`

const TitleSection = styled.section`
  width: 100%;
  padding: 2.5em;
  display: flex;
  justify-content: start;
  background-color: ${({ theme }) => theme.colors.neutrals[100]};
`

const Container = styled.div`
  display: flex;
  min-height: calc(100vh - 80px);
  align-items: center;
  justify-content: start;
  flex-direction: column;
`

export default Team
