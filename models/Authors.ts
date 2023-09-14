export interface Author {
  authorId: string
  documents: {
    description: string
    title: string
  }[]
  fullName: string
  orcid: string | null
  university: string
}

export type AuthorData = Pick<Author, 'fullName' | 'university' | 'orcid'>
export type AuthorDocs = Pick<Author, 'documents'>
