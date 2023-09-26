import { NextResponse } from 'next/server'

import type { NextRequest } from 'next/server'
import type { RequestCookies } from 'next/dist/server/web/spec-extension/cookies'
import { Theme } from '@/models/Utils'

const isLanguageSet = (cookies: RequestCookies) => {
  return cookies.get('NEXT_LOCALE')
}

const isThemeSet = (cookies: RequestCookies) => {
  return cookies.get('THEME')
}

export function middleware(req: NextRequest) {
  if (!isThemeSet(req.cookies)) {
    const response = NextResponse.next()

    response.cookies.set('THEME', Theme.light)

    return response
  }
  if (!isLanguageSet(req.cookies)) {
    const response = NextResponse.next()

    response.cookies.set('NEXT_LOCALE', req.nextUrl.locale)

    return response
  }

  /**
   * Allow serving health endpoint.
   */
  const { pathname } = req.nextUrl

  /**
   * Prevent the sending of forwarded cookies to analytics.
   * https://github.com/4lejandrito/next-plausible#proxy-the-analytics-script
   */
  if (pathname.startsWith('/proxy/api/event')) {
    const requestHeaders = new Headers(req.headers)
    requestHeaders.set('cookie', '')
    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    })
  }

  if (
    pathname.startsWith('/api/health') ||
    pathname.startsWith('/frontend/health')
  )
    return NextResponse.next()
}
