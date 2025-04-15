import { axios, withApiOptions } from '@/utils/api/axios'
import { SearchResponse, SearchRequest } from '@/models/Api'

export const searchAuthors = withApiOptions<SearchResponse, [SearchRequest]>(
  ({ baseUrl, headers }, { teamSize, prompt }) => {
    return axios.get(
      `${baseUrl}/api/author/search/?team_size=${teamSize}&q=${prompt}`,
      { headers }
    )
  }
)
