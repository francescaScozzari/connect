import { createSlice } from '@reduxjs/toolkit'
import type { Author } from '@/models/Authors'

interface SearchState {
  authors: Author[]
  q: string
  teamSize: number
}

const initialState: SearchState = { authors: [], q: '', teamSize: 0 }

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    setTeam: (state, action) => {
      state.authors = action.payload.authors
      state.q = action.payload.q
      state.teamSize = action.payload.teamSize
    }
  }
})

export const { setTeam } = searchSlice.actions

export default searchSlice.reducer
