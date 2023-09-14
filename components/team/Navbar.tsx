import React from 'react'
import styled from 'styled-components'
import Link from 'next/link'

import { Text } from '@/components/commons/Typography'
import { SmallLogo } from '@/components/home/Logo'
import { Button } from '@/components//commons/Button'
import { IconArrowBack } from '../commons/Icons'

const Navbar = () => {
  return (
    <Nav>
      <Link href="/">
        <SmallLogo title="BI4E" />
      </Link>

      <Link href="/">
        <Button>
          <IconArrowBack title="back" />
          <Label as="span" uppercase>
            Back to the search page
          </Label>
        </Button>
      </Link>
    </Nav>
  )
}

const Label = styled(Text.Normal)``

const Nav = styled.nav`
  width: 100%;
  background-color: white;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 2em 3em;
  border-bottom: 1px solid black;

  a {
    color: black;
    text-decoration: none;
  }

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
