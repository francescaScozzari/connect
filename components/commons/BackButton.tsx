import React from 'react'
import styled from 'styled-components'

import { IconSearch } from './Icons'
import { Text } from './Typography'

export const BackButton = () => {
  return (
    <Button>
      <IconSearch title="back" />
      <Label as="span">make a new search</Label>
    </Button>
  )
}

const Label = styled(Text.Normal)`
  text-transform: uppercase;
  font-weight: 600;
  line-height: normal;
  color: white;
`

const Button = styled.button`
  all: unset;
  display: flex;
  justify-content: center;
  align-content: center;
  border-radius: 10px;
  cursor: pointer;
  width: fit-content;
  outline: none;
  padding: 0.75em 1em;
  gap: 1em;
  transition: 0.3s background-color ease-in-out;
  background-color: ${({ theme }) => theme.colors.secondary[0]};

  &:disabled {
    cursor: not-allowed;
    opacity: 0.4;
  }
`
