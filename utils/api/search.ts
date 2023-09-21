import { axios, withApiOptions } from '@/utils/api/axios'
import type * as T from '@/models/Api'
import { SearchResponse } from '@/models/Api'

export const searchAuthors = withApiOptions<SearchResponse, [T.SearchRequest]>(
  ({ baseUrl, headers }, { teamSize, prompt }) => {
    return axios.get(
      `${baseUrl}/api/author/search/?team_size=${teamSize}&q=${prompt}`,
      { headers }
    )
  }
)
