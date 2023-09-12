import React, { useRef } from 'react'
import { styled } from 'styled-components'
import { useRouter } from 'next/router'
import { AxiosError } from 'axios'
import { toast } from 'react-toastify'
import { useForm } from 'react-hook-form'
import type { SubmitHandler } from 'react-hook-form'

import { Text } from '@/components/commons/Typography'
import { searchAuthors } from '@/utils/api/search'
import { useAppDispatch } from '@/store'
import { setTeam } from '@/store/searchSlice'
import { IconArrowSubmit, IconCrossReset, IconSearch } from '../commons/Icons'
import { useDynamicHeight } from '@/hooks'

type FormValues = {
  q: string
}

const SearchForm = () => {
  const {
    register,
    reset,
    handleSubmit,
    formState: { errors, isSubmitting, isValid }
  } = useForm<FormValues>({ mode: 'onChange' })

  const textAreaRef = useRef<HTMLTextAreaElement | null>(null)
  const heightKeeperRef = useRef<HTMLDivElement | null>(null)
  const { push } = useRouter()
  const dispatch = useAppDispatch()
  const { ref, ...rest } = register('q', {
    required: 'A search prompt is required',
    maxLength: 1024
  })

  useDynamicHeight(textAreaRef?.current, heightKeeperRef?.current)

  const onSubmit: SubmitHandler<FormValues> = async body => {
    const { q } = body

    searchAuthors({}, { teamSize: 6, prompt: q })
      .then(({ data }) => {
        dispatch(setTeam({ authors: data, q: q }))
        push('/team')
      })
      .catch(err => {
        if (err instanceof AxiosError) {
          toast.error(
            err.response
              ? `Oops! Something went wrong while fetching data. Please check your internet connection and try again`
              : null
          ),
            {
              position: toast.POSITION.TOP_CENTER,
              autoClose: 5000
            }
        }
      })
  }

  return (
    <>
      <Form onSubmit={handleSubmit(onSubmit)} role="search">
        <Wrapper>
          <HeightKeeper ref={heightKeeperRef} />
          <Input
            id="q"
            placeholder="Search here to find your research team"
            role="textarea"
            ref={e => {
              ref(e)
              textAreaRef.current = e
            }}
            {...rest}
          />
          {errors.q?.type === 'maxLength' ? (
            <Text.NormalBold role="alert">
              Search prompt too long
            </Text.NormalBold>
          ) : null}
          <Placeholder isFilled={textAreaRef?.current?.value} title="search" />
          <ClearButton  
            type="button"
            role="reset"
            isFilled={textAreaRef?.current?.value}
            onClick={() => {
              reset()
              textAreaRef?.current?.dispatchEvent(new Event('input'))
            }}
          >
            <div>
              <IconCrossReset title="reset" />
            </div>
          </ClearButton>
          <SubmitButton
            type="submit"
            role="submit"
            disabled={isSubmitting || !isValid}
          >
            <IconArrowSubmit title="submit" />
          </SubmitButton>
        </Wrapper>
      </Form>
    </>
  )
}

const Placeholder = styled(IconSearch)<{ isFilled: string | undefined }>`
  display: ${({ isFilled }) => (isFilled?.length ? 'none' : 'block')};
  position: absolute;
  top: calc(6em / 2);
  left: 5%;
  transform: translate(-50%, -50%);

  @media (max-width: 1280px) {
    top: calc(6em / 2);
  }

  @media (max-width: 768px) {
    top: calc(6.125em / 2);
    left: 7%;
  }
`

const HeightKeeper = styled.div`
  display: none;
`

const ClearButton = styled.button<{ isFilled: string | undefined }>`
  all: unset;
  display: ${({ isFilled }) => (isFilled?.length  ? 'block' : 'none')};
  position: absolute;
  top: calc(6em / 2);
  left: 5%;
  transform: translate(-50%, -50%);

  @media (max-width: 1280px) {
    top: calc(6em / 2);
  }

  @media (max-width: 768px) {
    top: calc(6.125em / 2);
    left: 7%;
  }
`

const SubmitButton = styled.button`
  width: 4.5em;
  height: 4.5em;
  border: 2px solid black;
  border-radius: 50%;
  position: absolute;
  top: calc(5.75em / 2);
  right: 0;
  transform: translate(-50%, -50%);

  &:disabled {
    opacity: 0.3;
  }

  @media (max-width: 1280px) {
    top: calc(5.5em / 2);
  }

  @media (max-width: 768px) {
    width: 4em;
    height: 4em;
    top: calc(5.5em / 2);
  }
`

const Wrapper = styled.div`
  display: flex;
  position: relative;
  flex-direction: column;
  gap: 2em;
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

const Input = styled.textarea`
  position: relative;
  flex-grow: 1;
  resize: none;
  overflow: hidden;
  border: 2px solid black;
  border-radius: 3.5em;
  box-sizing: border-box;
  width: 52em;
  padding: 1.75em 6.25em 0.75em 4.625em;
  line-height: 1.375;
  font-size: 1.125rem;

  &::placeholder {
    opacity: 1;
  }

  @media (max-width: 1280px) {
    width: 42em;
    padding: 1.625em 6.25em 0.75em 4.625em;
  }

  @media (max-width: 768px) {
    font-size: 1em;
    width: 36em;
    padding: 2em 6.25em 0.75em 4.625em;
  }
`

export { SearchForm }
