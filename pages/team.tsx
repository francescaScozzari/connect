import React from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { H1 } from '@/components/commons/Typography'
import { Navbar } from '@/components/team/Navbar'
import { useAppSelector } from '@/store'
import { SearchResults } from '@/components/team/SearchResults'
import { EmptyPlaceholder } from '@/components/team/EmptyPlaceholder'

const Team: NextPage = () => {
  const { authors, q } = useAppSelector(state => state.search)

  return (
    <>
      <Navbar />
      <Container>
        <TitleSection>
          <H1.Medium color="white">Your research team</H1.Medium>
        </TitleSection>
        {authors.length ? (
          <SearchResults authors={authors} q={q} />
        ) : (
          <EmptyPlaceholder />
        )}
      </Container>
    </>
  )
}

const TitleSection = styled.section`
  width: 100%;
  padding: 2.5em;
  background-color: ${({ theme }) => theme.colors.primary[0]};
`

const Container = styled.div`
  display: flex;
  min-height: calc(100vh - 80px);
  align-items: center;
  justify-content: start;
  flex-direction: column;
`

export default Team
