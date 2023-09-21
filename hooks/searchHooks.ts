import { useCallback, useEffect } from 'react'
import { Author } from '@/models/Authors'
import { SearchResponse } from '@/models/Api'

export function useDynamicHeight(
  element: HTMLTextAreaElement | null,
  heightKeeper: HTMLDivElement | null
) {
  const setHeight = useCallback(() => {
    if (element && heightKeeper) {
      element.style.height = 'inherit'
      element.style.height = element.scrollHeight + 'px'
      heightKeeper.style.height = element.scrollHeight + 'px'
    }
  }, [element?.scrollHeight])

  useEffect(() => {
    if (element && heightKeeper) {
      element.addEventListener('input', setHeight)
      heightKeeper.addEventListener('resize', setHeight)
      setHeight()
    }

    return () => {
      if (element && heightKeeper) {
        element.removeEventListener('input', setHeight)
        heightKeeper.removeEventListener('resize', setHeight)
      }
    }
  }, [element, heightKeeper])
}
