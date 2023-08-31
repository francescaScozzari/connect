import React from 'react'
import { styled } from 'styled-components'
import { useForm } from 'react-hook-form'
import type { SubmitHandler } from 'react-hook-form'
import { useRouter } from 'next/router'

import { Button } from '@/components/commons/Button'
import { Text } from '@/components/commons/Typography'
import { searchAuthors } from '@/utils/api/search'
import { useAppDispatch } from '@/store'
import { setTeam } from '@/store/searchSlice'
import { AxiosError } from 'axios'

type FormValues = {
  q: string
}

const SearchForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormValues>({ mode: 'onChange' })

  const { push } = useRouter()
  const dispatch = useAppDispatch()

  const onSubmit: SubmitHandler<FormValues> = async body => {
    const { q } = body

    searchAuthors({}, { teamSize: 6, prompt: q })
      .then(({ data }) => {
        dispatch(setTeam({ authors: data, q: q }))
        push('/team')
      })
      .catch(err => {
        if (err instanceof AxiosError) {
          console.log(err.toJSON())
        }
      })
  }

  return (
    <>
      <Form onSubmit={handleSubmit(onSubmit)} role="search">
        <Wrapper>
          <Input
            id="q"
            type="text"
            placeholder=""
            {...register('q', {
              required: 'A search prompt is required',
              maxLength: 1024
            })}
          />
          {errors.q?.type === 'required' ? (
            <Text.NormalBold role="alert">{errors.q?.message}</Text.NormalBold>
          ) : null}
          {errors.q?.type === 'maxLength' ? (
            <Text.NormalBold role="alert">
              Search prompt too long
            </Text.NormalBold>
          ) : null}
          <Button type="submit">Search</Button>
        </Wrapper>
      </Form>
    </>
  )
}

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5em;
  align-items: center;
`

const Form = styled.form`
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5em;
  p {
    margin-left: 0.625em;
    color: ${({ theme }) => theme.colors.status.error};
  }
`

const Input = styled.input<{ errors?: boolean }>`
  position: relative;
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

export { SearchForm }
