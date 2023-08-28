import React from 'react'
import styled from 'styled-components'
import type { NextPage } from 'next'

import { InputWithErrors } from '@/components/commons/Input'
import { H1 } from '@/components/commons/Typography'

const Home: NextPage = () => {
  return (
    <Container>
      <H1.Normal>Lorem Ipsum</H1.Normal>
      <InputWithErrors placeholder='' />
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
