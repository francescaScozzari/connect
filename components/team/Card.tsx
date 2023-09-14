import React from 'react'
import * as Accordion from '@radix-ui/react-accordion'

import { AccordionHeader } from './accordion/AccordionHeader'
import { AccordionContent } from './accordion/AccordionContent'

const Card = () => {
  return (
    <Accordion.Root type="single" defaultValue="item-1" collapsible>
      <Accordion.Item value="item-1">
        <AccordionHeader />
        <AccordionContent>
          Yes. It adheres to the WAI-ARIA design pattern.
        </AccordionContent>
      </Accordion.Item>

      <Accordion.Item value="item-2">
        <AccordionHeader>Is it unstyled?</AccordionHeader>
        <AccordionContent>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </AccordionContent>
      </Accordion.Item>

      <Accordion.Item value="item-3">
        <AccordionHeader>Is it unstyled?</AccordionHeader>
        <AccordionContent>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </AccordionContent>
      </Accordion.Item>

      <Accordion.Item value="item-4">
        <AccordionHeader>Is it unstyled?</AccordionHeader>
        <AccordionContent>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </AccordionContent>
      </Accordion.Item>

      <Accordion.Item value="item-5">
        <AccordionHeader>Is it unstyled?</AccordionHeader>
        <AccordionContent>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </AccordionContent>
      </Accordion.Item>

      <Accordion.Item value="item-6">
        <AccordionHeader>Is it unstyled?</AccordionHeader>
        <AccordionContent>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </AccordionContent>
      </Accordion.Item>

      <Accordion.Item value="item-7">
        <AccordionHeader>Is it unstyled?</AccordionHeader>
        <AccordionContent>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </AccordionContent>
      </Accordion.Item>
    </Accordion.Root>
  )
}

export { Card }
