import React from 'react'
import { styled } from 'styled-components'
import * as Accordion from '@radix-ui/react-accordion'

import { Text } from '@/components/commons/Typography'
import { IconArrowBack } from '@/components/commons/Icons'
import type { AuthorData } from '@/models/Authors'

const AccordionHeader = React.forwardRef<HTMLButtonElement, AuthorData>(
  ({ fullName, university, orcid }, forwardedRef) => (
    <CustomAccordionHeader>
      <AuthorData>
        <Text.NormalBold>{fullName}</Text.NormalBold>
        <Separator />
        <Container>
          <ShortText>{university}</ShortText>
          <Text.Normal>
            ORCID:{' '}
            <Text.NormalBold as="span">{orcid ? orcid : '-'}</Text.NormalBold>
          </Text.Normal>
        </Container>
      </AuthorData>
      <CustomAccordionTrigger ref={forwardedRef}>
        <IconArrowBack title="open" aria-hidden />
      </CustomAccordionTrigger>
    </CustomAccordionHeader>
  )
)

const ShortText = styled(Text.Normal)`
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 20em;
`

const Container = styled.div`
  display: flex;
  flex-flow: nowrap;
  justify-content: space-between;
`

const Separator = styled.div`
  width: 100%;
  height: 1px;
  background-color: black;
`

const AuthorData = styled.div`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-content: start;
  gap: 1em;
`

const CustomAccordionHeader = styled(Accordion.Header)`
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5em;
  padding: 1.5em;
  border: 2px solid black;
  border-top-left-radius: 1.875em;
  border-top-right-radius: 1.875em;
  margin-bottom: 0;

  &[data-state='closed'] {
    border-radius: 1.875em;
  }
`

const CustomAccordionTrigger = styled(Accordion.Trigger)`
  all: unset;
  padding: 0.25em;
  height: 1.375em;
  width: 1.375em;
  border: 2px solid black;
  border-radius: 50%;

  svg {
    transform: rotate(-90deg);
  }

  &[data-state='open'] > svg {
    transform: rotate(90deg);
  }
`
export { AccordionHeader }
