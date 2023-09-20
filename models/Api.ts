export interface ApiOptions {
  serverSide: boolean
}

export interface SearchRequest {
  teamSize: number
  prompt: string
}

export interface SearchResponse {
  q: string
}
