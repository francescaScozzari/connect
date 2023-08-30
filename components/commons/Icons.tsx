import React from 'react'

type Props = {
  title: string
} & React.ComponentPropsWithoutRef<'svg'>

const IconArrowCircle = ({ title, ...props }: Props) => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" {...props}>
      <title>{title}</title>
      <path d="M12 1a11 11 0 1 0 11 11A11 11 0 0 0 12 1Zm4.707 9.707a1 1 0 0 1-1.414 0L13 8.414V18a1 1 0 0 1-2 0V8.414l-2.293 2.293a1 1 0 1 1-1.414-1.414l4-4a1 1 0 0 1 1.414 0l4 4a1 1 0 0 1 0 1.414Z" />
    </svg>
  )
}

export { IconArrowCircle }
