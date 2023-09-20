import React from 'react'
import styled from 'styled-components'
import { toast } from 'react-toastify'
import { useRouter } from 'next/router'
import { AxiosError } from 'axios'
import type { NextPage } from 'next'

import { SearchForm } from '@/components/home/SearchForm'
import { BigLogo } from '@/components/commons/Logo'
import { SearchTips } from '@/components/commons/SearchTips'
import { searchAuthors } from '@/utils/api'
import { useAppDispatch } from '@/store'
import { setTeam } from '@/store/searchSlice'

const Home: NextPage = () => {
  const dispatch = useAppDispatch()
  const { push } = useRouter()

  return (
    <Container>
      <BigLogo title="BI4E" />
      <SearchForm
        handleSubmit={async body => {
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
        }}
      />
      <SearchTips />
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
`

export default Home
