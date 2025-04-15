import React from 'react'
import { styled } from 'styled-components'
import Link from 'next/link'

import { IconNoGroup } from '@/components/commons/Icons'
import { H2 } from '../commons/Typography'
import { BackButton } from '../commons/BackButton'
import { SearchTips } from '../commons/SearchTips'
import { AuthorsCounter } from './AuthorsCounter'

const EmptyPlaceholder = () => {
  return (
    <MainSection>
      <AuthorsCounter counter={0} />
      <Container>
        <IconNoGroup title="no team" />
        <H2.Normal color="#2B2D42">Your search returned no results</H2.Normal>
        <Link href="/">
          <BackButton />
        </Link>
        <SearchTips />
      </Container>
    </MainSection>
  )
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 2em;
  padding: 4em;
  border-radius: 20px;
  background-color: white;
`

const MainSection = styled.section`
  width: 100%;
  padding: 4em;
  display: flex;
  flex-direction: column;
  justify-content: start;
  gap: 1em;
  background-color: ${({ theme }) => theme.colors.primary[0]};
`

export { EmptyPlaceholder }
