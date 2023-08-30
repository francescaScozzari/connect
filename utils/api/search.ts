import { axios, withApiOptions } from '@/utils/api/axios'
import type * as T from '@/models/Api'
import type { Author } from '@/models/Authors'

export const searchAuthors = withApiOptions<Author[], [T.SearchRequest]>(
  ({ baseUrl, headers }, { teamSize, prompt }) => {
    return axios.get(
      `${baseUrl}/api/author/search/?team_size=${teamSize}&q=${prompt}`,
      { headers }
    )
  }
)
