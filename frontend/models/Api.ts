import { Author } from './Authors'

export interface ApiOptions {
  serverSide: boolean
}

export interface SearchRequest {
  teamSize: number
  prompt: string
}

export interface SearchResponse {
  authors: { authors: Author[] }
  givenSentence: { text: string; highlights: string[] }
}
