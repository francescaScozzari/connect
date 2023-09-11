import React from 'react'
import { styled } from 'styled-components'

const Footer = () => {
  return (
    <OuterWrapper>
      <FooterLink>© 2023 all rights reserved UDA CONNECT (TBD)</FooterLink>
      <InnerWrapper>
        <FooterLinkVariant>Privacy Policy</FooterLinkVariant>
        <FooterLinkVariant
          data-cy="ingenium"
          href="https://ingenium-eu.education/"
        >
          Ingenium University
        </FooterLinkVariant>
        <FooterLinkVariant data-cy="bi4e" href="https://boosting-ingenium.com/">
          BI4E
        </FooterLinkVariant>
      </InnerWrapper>
    </OuterWrapper>
  )
}

const OuterWrapper = styled.footer`
  min-height: 4.5em;
  padding: 2em 4.5em;
  display: flex;
  justify-content: space-between;

  @media (max-width: 1280px) {
    padding: 2em 3.5em;
  }

  @media (max-width: 768px) {
    padding: 2em 2em;
  }
`

const InnerWrapper = styled.footer`
  display: flex;
  gap: 2em;

  @media (max-width: 1280px) {
    gap: 1.5em;
  }

  @media (max-width: 768px) {
    gap: 0.5em;
  }
`

const FooterLink = styled.a`
  color: black;
  font-size: 0.75rem;
  text-transform: capitalize;
`
const FooterLinkVariant = styled(FooterLink)`
  text-decoration: underline;
`

export { Footer }
