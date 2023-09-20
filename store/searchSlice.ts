import { createSlice } from '@reduxjs/toolkit'
import type { Author } from '@/models/Authors'

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
    }
  }
})

export const { setTeam } = searchSlice.actions

export default searchSlice.reducer
