import React from 'react'
import styled from 'styled-components'
import GridLoader from 'react-spinners/GridLoader'

import { H2 } from '@/components/commons/Typography'

export const Spinner = ({ spinnerLoading }: { spinnerLoading: boolean }) => {
  return (
    <FloatingCointainer>
      <Wrapper>
        <GridLoader color={'#CE2F7C'} size={40} loading={spinnerLoading} />
        <H2.Normal color="white">We are searching...</H2.Normal>
      </Wrapper>
    </FloatingCointainer>
  )
}

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1em;
  position: absolute;
  z-index: 1000;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
`

const FloatingCointainer = styled.div`
  background-color: ${({ theme }) => theme.colors.primary[0]};
  position: absolute;
  z-index: 500;
  height: calc(100vh + 80px);
  width: 100%;
`
