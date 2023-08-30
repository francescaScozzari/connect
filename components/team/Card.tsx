import React from 'react'
import { styled } from 'styled-components'

import { Text } from '@/components/commons/Typography'
import { IconArrowCircle } from '@/components/commons/Icons'

type Props = {
  fullName: string
  university: string
}

const Card = ({ fullName, university }: Props) => {
  return (
    <Container>
      <Text.NormalBold>{fullName}</Text.NormalBold>
      <Text.Normal>{university}</Text.Normal>
      <IconArrowCircle title="Author details" width={24} height={24} />
    </Container>
  )
}

const Container = styled.div`
  display: flex;
  width: 20em;
  flex-direction: column;
  align-content: start;
  padding: 1.5em 1em 3em;
  border: 2px solid black;
  border-radius: 1em;
  gap: 0.5em;

  svg {
    margin-top: 1em;
    align-self: end;
    transform: rotate(90deg);
  }
`

export { Card }
