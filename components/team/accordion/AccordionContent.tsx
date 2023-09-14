import * as Accordion from '@radix-ui/react-accordion'
import React from 'react'
import { styled } from 'styled-components'

import { Text } from '@/components/commons/Typography'

const AccordionContent = React.forwardRef<
  HTMLDivElement,
  Accordion.AccordionContentProps
>(({ children, ...props }, forwardedRef) => (
  <CustomAccordionContent {...props} ref={forwardedRef}>
    <Container>
      <Text.NormalBold>
        Donec luctus eget lorem non hendrerit vestibulum in mi facilisis
      </Text.NormalBold>
      <Text.Normal>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut non purus
        nunc. Aliquam erat volutpat. Suspendisse blandit ex id velit iaculis, a
        pellentesque tellus bibendum. Mauris accumsan ex in feugiat vehicula.
        [...] na sit amet est euismod dictum at at ligula. Nunc sed arcu in
        turpis faucibus imperdiet. Mauris vehicula est urna, eget sagittis
        sapien vestibulum dapibus [...] hendrerit ac eros eu porta aliquet
        dapibus rhoncus.
      </Text.Normal>
    </Container>
  </CustomAccordionContent>
))

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1em;
  padding: 2em;
  background-color: ${({ theme }) => theme.colors.neutrals[100]};
`

const CustomAccordionContent = styled(Accordion.Content)`
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 2px solid black;
  border-top: 0;

  &[data-state='closed'] {
    border: 0;
  }
`

export { AccordionContent }
