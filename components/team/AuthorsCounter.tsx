import React from 'react'
import { styled } from 'styled-components'
import { IconGroup } from '@/components/commons/Icons'

const AuthorsCounter = ({ counter }: { counter: number }) => {
  return (
    <Label>
      <IconGroup title="group" />
      <Bold as="span">{counter}</Bold> researchers identified
    </Label>
  )
}

const Label = styled.span`
  gap: 1em;
  font-size: 0.875rem;
  color: white;
`

const Bold = styled(Label)`
  margin-left: 0.5em;
  font-weight: 700;
`

export { AuthorsCounter }
