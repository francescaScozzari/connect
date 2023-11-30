import React, { useRef } from 'react'
import { styled } from 'styled-components'
import { useForm } from 'react-hook-form'
import type { SubmitHandler } from 'react-hook-form'

import { Text } from '@/components/commons/Typography'
import {
  IconArrowSubmit,
  IconCrossReset,
  IconMinus,
  IconPlus,
  IconSearchPlaceholder
} from '@/components/commons/Icons'
import { useDynamicHeight } from '@/hooks'
import { usePlausible } from 'next-plausible'
import { TeamFilter } from './TeamFilter'

type FormValues = {
  givenSentence: string
  teamSize: number
}

type Props = {
  handleSubmit: (body: FormValues) => void
}

const SearchForm = ({ handleSubmit }: Props) => {
  const {
    register,
    reset,
    setValue,
    getValues,
    handleSubmit: handleHookFormSubmit,
    formState: { errors, isSubmitting, isSubmitted, isValid }
  } = useForm<FormValues>({ defaultValues: { teamSize: 5 }, mode: 'onChange' })

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
  }

  const plausible = usePlausible()

  return (
    <Form onSubmit={handleHookFormSubmit(onSubmit)} role="search" ref={formRef}>
      <TeamFilter>
        <TeamButton
          type="button"
          disabled={isSubmitting || isSubmitted || getValues('teamSize') <= 5}
          onClick={() => {
            const value = getValues('teamSize')

            setValue('teamSize', value - 1, {
              shouldValidate: true
            })
          }}
        >
          <IconMinus title="minus" />
        </TeamButton>
        <TeamInput
          readOnly
          inputMode="numeric"
          {...register('teamSize', {
            max: 20,
            min: 5
          })}
        />
        <TeamButton
          type="button"
          disabled={isSubmitting || isSubmitted || getValues('teamSize') >= 20}
          onClick={() => {
            const value = getValues('teamSize')

            setValue('teamSize', value + 1, {
              shouldValidate: true
            })
          }}
        >
          <IconPlus title="plus" />
        </TeamButton>
      </TeamFilter>

      <Wrapper>
        <HeightKeeper ref={heightKeeperRef} />
        <SearchInput
          id="q"
          placeholder="Search here to find your research team"
          role="textarea"
          ref={e => {
            ref(e)
            textAreaRef.current = e
          }}
          rows={1}
          onKeyDown={e => {
            if (e.key === 'Enter' && e.shiftKey == false) {
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
  padding: 1.125em;
  top: calc(57.5% - 3.125em);
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

const TeamButton = styled.button`
  border: 2px solid transparent;
  border-radius: 50%;
  background-color: ${({ theme }) => theme.colors.secondary[0]};
  padding: 0.3em 0.375em;

  &:disabled {
    background-color: white;
    border-color: rgb(36 36 36 / 0.25);

    svg path {
      stroke: rgb(36 36 36 / 0.25);
    }
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
    color: ${({ theme }) => theme.colors.status.error};
  }
`

const SearchInput = styled.textarea`
  position: relative;
  flex-grow: 1;
  resize: none;
  overflow: hidden;
  border: 1px solid #e5e5e5;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  border-radius: 3.5em;
  box-sizing: border-box;
  width: 47.5em;
  padding: 2em 7.75em 2em 4.875em;
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

const TeamInput = styled.input`
  position: relative;
  flex-grow: 1;
  resize: none;
  overflow: hidden;
  border: 1px solid #e5e5e5;
  border-radius: 3.5em;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  height: 2.5em;
  text-align: center;
`

export { SearchForm }
