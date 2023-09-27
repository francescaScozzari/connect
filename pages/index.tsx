import React, { useEffect, useState } from 'react'
import styled from 'styled-components'
import { toast } from 'react-toastify'
import { useRouter } from 'next/router'
import { AxiosError } from 'axios'
import type { NextPage } from 'next'

import { SearchForm } from '@/components/home/SearchForm'
import { BigLogo } from '@/components/commons/Logo'
import { SearchTips } from '@/components/commons/SearchTips'
import { searchAuthors } from '@/utils/api'
import { Spinner } from '@/components/home/Spinner'

const Home: NextPage = () => {
  const { push } = useRouter()

  const [spinnerLoading, setSpinnerLoading] = useState(false)

  useEffect(() => {
    localStorage.clear()
  }, [])

  return (
    <Container>
      <BigLogo title="BI4E" />
      {spinnerLoading && <Spinner spinnerLoading={spinnerLoading} />}
      <SearchForm
        handleSubmit={async body => {
          const { givenSentence } = body

          setSpinnerLoading(true)

          searchAuthors({}, { teamSize: 20, prompt: givenSentence })
            .then(({ data }) => {
              const { authors, givenSentence } = data
              localStorage.setItem(
                'data',
                JSON.stringify({
                  authors: authors,
                  givenSentence: givenSentence
                })
              )
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
            .finally(() => {
              setSpinnerLoading(false)
              push('/team')
            })
        }}
      />
      <SearchTips titleColor="#C9D2EC" textColor="white" />
    </Container>
  )
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 3em;
  min-height: calc(100vh - 80px);
  align-items: center;
  justify-content: center;
  background-color: ${({ theme }) => theme.colors.primary[0]};

  svg {
  }
`

export default Home
