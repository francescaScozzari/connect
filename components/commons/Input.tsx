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
  border: 1px solid black;
  box-sizing: border-box;
  border-radius: 0.375em;
  padding: 0.625em 2em;
  width: 25em;
  font-style: normal;
  font-size: 1.125rem;
  &::placeholder {
    padding-left: 1.5em;
    font-size: 1.125rem;
    background: url("data:image/svg+xml,%3Csvg width='18' height='18' viewBox='0 0 18 18' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M16.6 18L10.3 11.7C9.8 12.1 9.225 12.4167 8.575 12.65C7.925 12.8833 7.23333 13 6.5 13C4.68333 13 3.146 12.371 1.888 11.113C0.629333 9.85433 0 8.31667 0 6.5C0 4.68333 0.629333 3.14567 1.888 1.887C3.146 0.629 4.68333 0 6.5 0C8.31667 0 9.85433 0.629 11.113 1.887C12.371 3.14567 13 4.68333 13 6.5C13 7.23333 12.8833 7.925 12.65 8.575C12.4167 9.225 12.1 none9.8 11.7 10.3L18 16.6L16.6 18ZM6.5 11C7.75 11 8.81267 10.5627 9.688 9.688C10.5627 8.81267 11 7.75 11 6.5C11 5.25 10.5627 4.18733 9.688 3.312C8.81267 2.43733 7.75 2 6.5 2C5.25 2 4.18733 2.43733 3.312 3.312C2.43733 4.18733 2 5.25 2 6.5C2 7.75 2.43733 8.81267 3.312 9.688C4.18733 10.5627 5.25 11 6.5 11Z' fill='%23C7C7C7'/%3E%3C/svg%3E")
      no-repeat 0.5em center;
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
