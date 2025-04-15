import React from 'react'
import * as Accordion from '@radix-ui/react-accordion'

import { AccordionHeader } from './accordion/AccordionHeader'
import { AccordionContent } from './accordion/AccordionContent'
import { Author } from '@/models/Authors'

type CardProps = {
  authors: Author[]
}

const Card = ({ authors }: CardProps) => {
  return (
    <Accordion.Root type="single" defaultValue="item-0" collapsible>
      {authors.map((author, index) => {
        return (
          <Accordion.Item key={index} value={`item-${index}`}>
            <AccordionHeader
              fullName={author.fullName}
              university={author.university}
              orcid={author?.orcid}
            />
            <AccordionContent documents={author.documents} />
          </Accordion.Item>
        )
      })}
    </Accordion.Root>
  )
}

export { Card }
