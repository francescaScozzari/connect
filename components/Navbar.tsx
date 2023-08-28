import React from 'react'
import styled from 'styled-components'

import { ThemeSwitch } from '@/components/ThemeSwitch'

const Navbar = () => {
  return (
    <Nav>
      <ThemeSwitch />
    </Nav>
  )
}

const Nav = styled.nav`
  width: 100%;
  background-color: ${({ theme }) => theme.colors.neutrals[100]};
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 5px;
`

export { Navbar }
