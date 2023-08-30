import React from 'react'
import styled from 'styled-components'

type Props = JSX.IntrinsicElements['input'] & {
  errors?: string[]
}

const InputWithErrors = ({
  errors,
  max,
  min,
  onChange,
  placeholder,
  required,
  step,
  style,
  type,
  value
}: Props) => {
  return (
    <InputContainer style={style}>
      <Input
        errors={errors && errors.length > 0}
        max={max}
        min={min}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        step={step}
        type={type}
        value={value}
      />
      {errors && errors.length > 0 && errors.map(err => <p key={err}>{err}</p>)}
    </InputContainer>
  )
}

const Input = styled.input<{ errors?: boolean }>`
  border: 2px solid black;
  box-sizing: border-box;
  border-radius: 0.5em;
  padding: 0.625em 2em;
  width: 25em;
  font-style: normal;
  font-size: 1.125rem;
  &::placeholder {
    padding-left: 1.5em;
    font-size: 1.125rem;
    background: url("data:image/svg+xml,%3Csvg height='24' width='24' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cstyle%3E.cls-1%7Bfill:none;stroke:%23000;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px%7D%3C/style%3E%3C/defs%3E%3Cg id='_21.search'%3E%3Ccircle class='cls-1' cx='9' cy='9' r='8'/%3E%3Cpath class='cls-1' d='m15 15 8 8'/%3E%3C/g%3E%3C/svg%3E")
      no-repeat 0.5em center;
  }
  @media (max-width: 768px) {
    font-size: 1em;
    width: 15em;
  }
`

const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5em;
  p {
    font-size: 0.75em;
    margin-left: 0.625em;
    color: ${({ theme }) => theme.colors.status.error};
  }
`

export { Input, InputWithErrors }
