import * as Accordion from '@radix-ui/react-accordion'
import React from 'react'
import { styled } from 'styled-components'

import { Text } from '@/components/commons/Typography'
import type { AuthorDocs } from '@/models/Authors'

const AccordionContent = React.forwardRef<HTMLDivElement, AuthorDocs>(
  ({ documents }, forwardedRef) => (
    <CustomAccordionContent ref={forwardedRef}>
      {documents.map(doc => {
        return (
          <Container key={doc.title}>
            <Text.NormalBold>{doc.title}</Text.NormalBold>
            <Text.Normal>{doc.description}</Text.Normal>
          </Container>
        )
      })}
    </CustomAccordionContent>
  )
)

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1em;
  padding: 2em;
  width: 100%;
  background-color: ${({ theme }) => theme.colors.neutrals[100]};
  border-bottom: 2px solid black;
`

const CustomAccordionContent = styled(Accordion.Content)`
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 2px solid black;
  border-top: 0;
  border-bottom: 0;

  &[data-state='closed'] {
    border: 0;
  }
`

export { AccordionContent }
