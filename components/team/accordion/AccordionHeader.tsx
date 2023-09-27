import React from 'react'
import { styled } from 'styled-components'
import * as Accordion from '@radix-ui/react-accordion'

import { H3, Text } from '@/components/commons/Typography'
import { IconChevron, IconUni } from '@/components/commons/Icons'
import type { AuthorData } from '@/models/Authors'

const AccordionHeader = React.forwardRef<HTMLButtonElement, AuthorData>(
  ({ fullName, university, orcid }, forwardedRef) => (
    <CustomAccordionHeader>
      <AuthorData>
        <H3.Normal color="white">{fullName}</H3.Normal>
        <Container>
          <SubContainer>
            <IconUni title="author" />
            <ShortText color="white">{university}</ShortText>
          </SubContainer>
          <Paragraph color="white">
            ORCID <OrcidCode>{orcid ? orcid : '-'}</OrcidCode>
          </Paragraph>
        </Container>
      </AuthorData>
      <CustomAccordionTrigger ref={forwardedRef}>
        <IconChevron title="open" aria-hidden />
      </CustomAccordionTrigger>
    </CustomAccordionHeader>
  )
)

const Paragraph = styled(Text.NormalBold)`
  padding: 0.375em 0.5em;
  background-color: ${({ theme }) => theme.colors.primary[0]};
  border-radius: 1.25em;
`

const OrcidCode = styled.strong`
  text-transform: uppercase;
  font-size: normal;
  color: white;
`

const SubContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.25em;
`

const ShortText = styled(Text.MediumBold)`
  text-transform: uppercase;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 50em;

  @media (max-width: 1600px) {
    max-width: 28em;
  }

  @media (max-width: 1440px) {
    max-width: 16em;
  }
`

const Container = styled.div`
  display: flex;
  flex-flow: nowrap;
  justify-content: space-between;
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
  border: 1px solid #c9d2ec;
  border-top-left-radius: 1.25em;
  border-top-right-radius: 1.25em;
  background-color: #434660;
  margin-bottom: 0;

  &[data-state='closed'] {
    border-radius: 1.25em;
  }
`

const CustomAccordionTrigger = styled(Accordion.Trigger)`
  all: unset;
  padding: 0.375em;
  height: 1.375em;
  width: 1.375em;
  border: 2px solid #c9d2ec;
  border-radius: 50%;
  transform: rotate(180deg);

  &[data-state='open'] > svg {
    transform: rotate(-180deg);
  }
`
export { AccordionHeader }
