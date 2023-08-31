import React from 'react'
import styled from 'styled-components'
import Link from 'next/link'

import { InputWithErrors } from '@/components/commons/Input'
import { H3 } from '@/components/commons/Typography'
import { useAppSelector } from '@/store'

const Navbar = () => {
  const { q } = useAppSelector(state => state.search)

  return (
    <Nav>
      <H3.Normal>
        <Link href="/">Lorem Ipsum</Link>
      </H3.Normal>
      <InputWithErrors placeholder={q} />
    </Nav>
  )
}

const Nav = styled.nav`
  width: 100%;
  background-color: ${({ theme }) => theme.colors.neutrals[100]};
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 2em 3em;

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
