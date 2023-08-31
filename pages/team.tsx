import React from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { H2, Text } from '@/components/commons/Typography'
import { Button } from '@/components/commons/Button'
import { Navbar } from '@/components/team/Navbar'
import { Card } from '@/components/team/Card'
import { useAppSelector } from '@/store'

const Team: NextPage = () => {
  const { authors } = useAppSelector(state => state.search)

  return (
    <>
      <Navbar />
      <Container>
        <TeamSection>
          <H2.Normal>Team</H2.Normal>
          <Text.NormalBold>
            Abbiamo individuato per te un team multidisciplinare di 9 profili in
            linea con il tuo progetto di ricerca
          </Text.NormalBold>
          <CardsContainer>
            {authors?.map(author => {
              return (
                <Card
                  key={author.orcid}
                  fullName={author.fullName}
                  university={author.university}
                />
              )
            })}
          </CardsContainer>
          <SuggestionButton>Perchè ti suggeriamo questo team</SuggestionButton>
        </TeamSection>
      </Container>
    </>
  )
}

const TeamSection = styled.section`
  display: flex;
  align-items: start;
  justify-content: center;
  flex-direction: column;
  gap: 1em;
`

const Container = styled.div`
  display: flex;
  padding: 2.5em;
  gap: 3em;
  min-height: calc(100vh - 80px);
  align-items: center;
  justify-content: start;
  flex-direction: column;
`

const CardsContainer = styled.div`
  display: flex;
  flex-flow: row wrap;
  justify-content: space-around;
  margin-top: 1.5em;
  gap: 1.5em;
`

const SuggestionButton = styled(Button)`
  align-self: end;
  background-color: black;
`

export default Team
