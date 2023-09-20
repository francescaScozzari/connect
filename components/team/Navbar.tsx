import React from 'react'
import styled from 'styled-components'
import Link from 'next/link'

import { SmallLogo } from '@/components/commons/Logo'
import { BackButton } from '@/components//commons/BackButton'

const Navbar = () => {
  return (
    <Nav>
      <Link href="/">
        <SmallLogo title="BI4E" />
      </Link>

      <Link href="/">
        <BackButton />
      </Link>
    </Nav>
  )
}

const Nav = styled.nav`
  width: 100%;
  background-color: ${({ theme }) => theme.colors.primary[0]};
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 2em 3em;
  border-bottom: 1px solid #c9d2ec;

  div {
    margin: 0 auto;
  }

  @media (max-width: 768px) {
    div {
      display: none;
    }
  }
`

export { Navbar }
