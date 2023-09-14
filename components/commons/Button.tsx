import styled from 'styled-components'

export const Button = styled.button`
  align-items: center;
  background-color: white;
  border: 2px solid black;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  min-width: 120px;
  outline: none;
  padding: 1em 1.5em;
  gap: 1em;
  transition: 0.3s background-color ease-in-out;
  width: fit-content;

  &:disabled {
    cursor: not-allowed;
    opacity: 0.4;
  }
`
