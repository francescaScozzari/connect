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
            <Title>{doc.title}</Title>
            <Paragraph color="#242424">{doc.description}</Paragraph>
          </Container>
        )
      })}
    </CustomAccordionContent>
  )
)

const Title = styled.span`
  display: inline-block;
  color: ${({ theme }) => theme.colors.primary[0]};
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.5;
`

const Paragraph = styled(Text.Normal)`
  line-height: 2.25;
  text-align: start;
`

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1em;
  padding: 2em;
  width: 100%;
  background-color: ${({ theme }) => theme.colors.neutrals[100]};
  border-bottom: 1px solid #c9d2ec;
`

const CustomAccordionContent = styled(Accordion.Content)`
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #c9d2ec;
  border-top: 0;
  border-bottom: 0;

  &[data-state='closed'] {
    border: 0;
  }
`

export { AccordionContent }
