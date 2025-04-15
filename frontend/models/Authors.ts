export interface Author {
  authorId: string
  documents: {
    description: string
    doi: string
    highlights: string[]
    score: number
    title: string
  }[]
  fullName: string
  orcid: string
  score: number
  university: string
}

export type AuthorData = Pick<Author, 'fullName' | 'university' | 'orcid'>
export type AuthorDocs = Pick<Author, 'documents'>
