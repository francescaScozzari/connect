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

const IconArrowSubmit = ({ title, ...props }: Props) => {
  return (
    <svg
      width="45"
      height="45"
      viewBox="0 0 45 45"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g id="Arrow forward">
        <path
          id="Vector"
          d="M22.5 7.5L19.8563 10.1437L30.3188 20.625H7.5V24.375H30.3188L19.8563 34.8563L22.5 37.5L37.5 22.5L22.5 7.5Z"
          fill="black"
        />
      </g>
    </svg>
  )
}

const IconCrossReset = ({ title, ...props }: Props) => {
  return (
    <svg
      width="31"
      height="31"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="m24.5417 8.27962-1.8212-1.82125L15.5 13.6788 8.27962 6.45837 6.45837 8.27962 13.6788 15.5l-7.22043 7.2205 1.82125 1.8212L15.5 17.3213l7.2205 7.2204 1.8212-1.8212L17.3213 15.5l7.2204-7.22038Z"
          fill="#000"
        />
      </g>
    </svg>
  )
}

const IconCopy = ({ title, ...props }: Props) => {
  return (
    <svg
      width="49"
      height="49"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="M32.6673 2.04163H8.16732c-2.24584 0-4.08334 1.8375-4.08334 4.08333V34.7083h4.08334V6.12496H32.6673V2.04163Zm-2.0416 8.16667H16.334c-2.2458 0-4.0629 1.8375-4.0629 4.0833l-.0204 28.5834c0 2.2458 1.817 4.0833 4.0629 4.0833h22.4787c2.2459 0 4.0834-1.8375 4.0834-4.0833V22.4583l-12.25-12.25ZM16.334 42.875V14.2916h12.25V24.5h10.2083v18.375H16.334Z"
          fill="#000"
        />
      </g>
    </svg>
  )
}

const IconTarget = ({ title, ...props }: Props) => {
  return (
    <svg
      width="49"
      height="51"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <path
        d="M24.4993 16.9969c-4.512 0-8.1666 3.803-8.1666 8.4984s3.6546 8.4985 8.1666 8.4985c4.5121 0 8.1667-3.8031 8.1667-8.4985 0-4.6954-3.6546-8.4984-8.1667-8.4984Zm18.2525 6.3738c-.9391-8.8596-7.697-15.89205-16.2108-16.86937V4.24924c0-1.16853-.9187-2.12461-2.0417-2.12461-1.1229 0-2.0416.95608-2.0416 2.12461v2.25209C13.9439 7.47865 7.18602 14.5111 6.24685 23.3707H4.08268c-1.12291 0-2.04166.9561-2.04166 2.1246 0 1.1686.91875 2.1246 2.04166 2.1246h2.16417c.93917 8.8597 7.69705 15.8921 16.21085 16.8694v2.2521c0 1.1686.9187 2.1246 2.0416 2.1246 1.123 0 2.0417-.956 2.0417-2.1246v-2.2521c8.5138-.9773 15.2717-8.0097 16.2108-16.8694h2.1642c1.1229 0 2.0417-.956 2.0417-2.1246 0-1.1685-.9188-2.1246-2.0417-2.1246h-2.1642ZM24.4993 40.3676c-7.9012 0-14.2916-6.65-14.2916-14.8723 0-8.2222 6.3904-14.8722 14.2916-14.8722 7.9013 0 14.2917 6.65 14.2917 14.8722 0 8.2223-6.3904 14.8723-14.2917 14.8723Z"
        fill="#000"
      />
    </svg>
  )
}

export {
  IconArrowCircle,
  IconArrowSubmit,
  IconCrossReset,
  IconCopy,
  IconTarget
}
