import React, { useEffect, useState } from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { H1 } from '@/components/commons/Typography'
import { Navbar } from '@/components/team/Navbar'
import { SearchResults } from '@/components/team/SearchResults'
import { EmptyPlaceholder } from '@/components/team/EmptyPlaceholder'
import { Author } from '@/models/Authors'

const Team: NextPage = () => {
  const [data, setData] = useState<{
    authors: Author[]
    givenSentence: { text: string; highlights: string[] }
  }>({ authors: [], givenSentence: { text: '', highlights: [] } })

  useEffect(() => {
    const data = localStorage.getItem('data')
    if (data) setData(JSON.parse(data))
  }, [])

  return (
    <>
      <Navbar />
      <Container>
        <TitleSection>
          <H1.Medium color="white">Your research team</H1.Medium>
        </TitleSection>
        {data?.authors?.length ? (
          <SearchResults authors={data.authors} q={data.givenSentence.text} />
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
  background-color: ${({ theme }) => theme.colors.primary[0]};
`

export default Team
