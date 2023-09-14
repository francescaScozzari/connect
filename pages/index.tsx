import React from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { SearchForm } from '@/components/home/SearchForm'
import { BigLogo } from '@/components/home/Logo'
import { SearchTips } from '@/components/home/SearchTips'

const Home: NextPage = () => {
  return (
    <Container>
      <BigLogo title="BI4E" />
      <SearchForm />
      <SearchTips />
    </Container>
  )
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 3em;
  min-height: calc(100vh - 80px);
  align-items: center;
  justify-content: center;
`

export default Home
