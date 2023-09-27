import React, { useRef } from 'react'
import { styled } from 'styled-components'
import { useForm } from 'react-hook-form'
import type { SubmitHandler } from 'react-hook-form'

import { Text } from '@/components/commons/Typography'
import {
  IconArrowSubmit,
  IconCrossReset,
  IconSearchPlaceholder
} from '@/components/commons/Icons'
import { useDynamicHeight } from '@/hooks'
import { usePlausible } from 'next-plausible'

type FormValues = {
  givenSentence: string
}

type Props = {
  handleSubmit: (body: FormValues) => void
}

const SearchForm = ({ handleSubmit }: Props) => {
  const {
    register,
    reset,
    handleSubmit: handleHookFormSubmit,
    formState: { errors, isSubmitting, isSubmitted, isValid }
  } = useForm<FormValues>({ mode: 'onChange' })

  const textAreaRef = useRef<HTMLTextAreaElement | null>(null)
  const formRef = useRef<HTMLFormElement | null>(null)
  const heightKeeperRef = useRef<HTMLDivElement | null>(null)
  const { ref, ...rest } = register('givenSentence', {
    required: 'A search prompt is required',
    maxLength: 512
  })

  useDynamicHeight(textAreaRef?.current, heightKeeperRef?.current)

  const onSubmit: SubmitHandler<FormValues> = async body => {
    handleSubmit({ ...body })
    console.log(isSubmitted)
  }

  const plausible = usePlausible()

  return (
    <Form onSubmit={handleHookFormSubmit(onSubmit)} role="search" ref={formRef}>
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
          rows={1}
          onKeyDown={e => {
            if (e.key === 'Enter') {
              e.preventDefault()
              formRef?.current?.requestSubmit()
            }
          }}
          {...rest}
        />
        {errors.givenSentence?.type === 'maxLength' ? (
          <Text.NormalBold role="alert">Search prompt too long</Text.NormalBold>
        ) : null}
        <Placeholder
          $isFilled={textAreaRef?.current?.value}
          title="search"
          fill="#242424"
        />
        <ClearButton
          type="button"
          role="reset"
          $isFilled={textAreaRef?.current?.value}
          onClick={() => {
            reset()
            textAreaRef?.current?.dispatchEvent(new Event('input'))
          }}
        >
          <>
            <IconCrossReset title="reset" fill="#242424" />
          </>
        </ClearButton>
        <SubmitButton
          type="submit"
          role="submit"
          disabled={isSubmitting || isSubmitted || !isValid}
          onClick={() => plausible('searchClick')}
        >
          <IconArrowSubmit title="submit" />
        </SubmitButton>
      </Wrapper>
    </Form>
  )
}

const Placeholder = styled(IconSearchPlaceholder)<{
  $isFilled: string | undefined
}>`
  display: ${({ $isFilled }) => ($isFilled?.length ? 'none' : 'block')};
  position: absolute;
  top: calc(50% - 1.25em);
  left: calc(4.5em - 2.25em);

  @media (max-width: 1280px) {
    top: calc(50% - 1.25em);
  }

  @media (max-width: 768px) {
    top: calc(50% - 1.25em);
    left: calc(4.5em - 2.25em);
  }
`

const HeightKeeper = styled.div`
  display: none;
`

const ClearButton = styled.button<{ $isFilled: string | undefined }>`
  all: unset;
  display: ${({ $isFilled }) => ($isFilled?.length ? 'block' : 'none')};
  position: absolute;
  top: calc(50% - 1.25em);
  left: calc(4.5em - 2.25em);

  @media (max-width: 1280px) {
    top: calc(50% - 1.25em);
  }

  @media (max-width: 768px) {
    top: calc(50% - 1.25em);
    left: calc(4.5em - 2.25em);
  }
`

const SubmitButton = styled.button`
  border: 1px solid transparent;
  border-radius: 50%;
  background-color: ${({ theme }) => theme.colors.secondary[0]};
  position: absolute;
  padding: 1.5em;
  top: calc(50% - 3.125em);
  right: 0.75em;

  &:disabled {
    opacity: 0.5;
  }

  @media (max-width: 1280px) {
    top: calc(50% - 3.125em);
  }

  @media (max-width: 768px) {
    top: calc(50% - 3.125em);
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
  border: 1px solid #e5e5e5;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  border-radius: 3.5em;
  box-sizing: border-box;
  width: 47.5em;
  padding: 2.75em 7.75em 2.75em 4.875em;
  color: #242424;
  font-size: 1.125rem;
  line-height: normal;
  text-align: start;

  &::placeholder {
    opacity: 0.6;
  }

  @media (max-width: 1280px) {
    width: 42em;
  }

  @media (max-width: 768px) {
    width: 36em;
  }
`

export { SearchForm }
