import React from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { H1 } from '@/components/commons/Typography'
import { SearchForm } from '@/components/home/SearchForm'

const Home: NextPage = () => {
  return (
    <Container>
      <H1.Normal>Lorem Ipsum</H1.Normal>
      <SearchForm />
    </Container>
  )
}

const Container = styled.div`
  display: flex;
  gap: 3em;
  min-height: calc(100vh - 80px);
  align-items: center;
  justify-content: center;
  flex-direction: column;
`

export default Home
