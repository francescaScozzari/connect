import { createSlice } from '@reduxjs/toolkit'
import { Author } from '@/models/Authors'

interface SearchState {
  authors: Author[]
  q: string
}

const initialState: SearchState = { authors: [], q: '' }

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    setTeam: (state, action) => {
      state.authors = action.payload.authors
      state.q = action.payload.q
    },
    resetTeam: state => {
      state.authors = []
      state.q = ''
    }
  }
})

export const { setTeam } = searchSlice.actions

export default searchSlice.reducer
