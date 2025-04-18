import React from 'react'

type Props = {
  title: string
  fill?: string
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
      fill="white"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path d="M22.5 7.5L19.8563 10.1437L30.3188 20.625H7.5V24.375H30.3188L19.8563 34.8563L22.5 37.5L37.5 22.5L22.5 7.5Z" />
      </g>
    </svg>
  )
}

const IconCrossReset = ({ title, ...props }: Props) => {
  return (
    <svg
      width="40"
      height="40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="m31.666 10.683-2.35-2.35L20 17.65l-9.317-9.317-2.35 2.35L17.65 20l-9.317 9.317 2.35 2.35L20 22.35l9.316 9.317 2.35-2.35L22.35 20l9.316-9.317Z"
          fill="#515151"
        />
      </g>
    </svg>
  )
}

const IconNote = ({ title, color, ...props }: Props) => {
  return (
    <svg
      width="40"
      height="40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="M31.667 8.333v15h-8.334v8.334h-15V8.333h23.334Zm0-3.333H8.333A3.343 3.343 0 0 0 5 8.333v23.334C5 33.5 6.5 35 8.333 35H25l10-10V8.333C35 6.5 33.5 5 31.667 5ZM20 23.333h-8.333V20H20v3.333Zm8.333-6.666H11.667v-3.334h16.666v3.334Z"
          fill={color ?? '#2B2D42'}
        />
      </g>
    </svg>
  )
}

const IconTarget = ({ title, color, ...props }: Props) => {
  return (
    <svg
      width="40"
      height="40"
      fill="white"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="M20 13.333A6.665 6.665 0 0 0 13.333 20 6.665 6.665 0 0 0 20 26.667 6.665 6.665 0 0 0 26.666 20 6.665 6.665 0 0 0 20 13.333Zm14.9 5c-.767-6.95-6.284-12.466-13.233-13.233V1.667h-3.334V5.1c-6.95.767-12.466 6.283-13.233 13.233H1.667v3.334H5.1c.767 6.95 6.283 12.466 13.233 13.233v3.433h3.334V34.9c6.95-.767 12.466-6.283 13.233-13.233h3.433v-3.334H34.9ZM20 31.667A11.658 11.658 0 0 1 8.333 20C8.333 13.55 13.55 8.333 20 8.333S31.666 13.55 31.666 20 26.45 31.667 20 31.667Z"
          fill={color ?? '#2B2D42'}
        />
      </g>
    </svg>
  )
}

const IconChevron = ({ title, ...props }: Props) => {
  return (
    <svg width="25" height="24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g>
        <path
          d="m7.91 15.41 4.59-4.58 4.59 4.58L18.5 14l-6-6-6 6 1.41 1.41Z"
          fill="#C9D2EC"
        />
      </g>
    </svg>
  )
}

const IconSearch = ({ title, ...props }: Props) => {
  const svgStyle = {
    fill: 'none',
    stroke: 'white',
    strokeLineCap: 'round',
    strokeLineJoin: 'round',
    strokeWidth: '2px'
  }

  return (
    <svg height="24" width="24" xmlns="http://www.w3.org/2000/svg" {...props}>
      <title>{title}</title>
      <defs>
        <style></style>
      </defs>
      <g id="_21.search">
        <circle style={svgStyle} cx="9" cy="9" r="7" />
        <path style={svgStyle} d="m14 14 8 8" />
      </g>
    </svg>
  )
}

const IconSearchPlaceholder = ({ title, ...props }: Props) => {
  return (
    <svg
      width="40"
      height="40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="M25.833 23.333h-1.316l-.467-.45a10.786 10.786 0 0 0 2.617-7.05C26.667 9.85 21.817 5 15.833 5 9.85 5 5 9.85 5 15.833c0 5.984 4.85 10.834 10.833 10.834 2.684 0 5.15-.984 7.05-2.617l.45.467v1.316l8.334 8.317 2.483-2.483-8.317-8.334Zm-10 0a7.49 7.49 0 0 1-7.5-7.5c0-4.15 3.35-7.5 7.5-7.5s7.5 3.35 7.5 7.5-3.35 7.5-7.5 7.5Z"
          fill="#8F8F8F"
        />
      </g>
    </svg>
  )
}

const IconGroup = ({ title, fill, ...props }: Props) => {
  return (
    <svg
      width="26"
      height="14"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <path
        d="M4.333 8.083A2.173 2.173 0 0 0 6.5 5.917 2.173 2.173 0 0 0 4.333 3.75a2.173 2.173 0 0 0-2.166 2.167c0 1.191.975 2.166 2.166 2.166Zm1.224 1.192a7.565 7.565 0 0 0-1.224-.108 7.53 7.53 0 0 0-3.011.628A2.178 2.178 0 0 0 0 11.799V13.5h4.875v-1.744c0-.9.25-1.744.683-2.481Zm16.11-1.192a2.173 2.173 0 0 0 2.166-2.166 2.173 2.173 0 0 0-2.166-2.167A2.173 2.173 0 0 0 19.5 5.917c0 1.191.975 2.166 2.167 2.166ZM26 11.8c0-.877-.52-1.657-1.322-2.004a7.53 7.53 0 0 0-3.011-.628c-.423 0-.824.043-1.225.108.434.737.683 1.582.683 2.48V13.5H26v-1.7Zm-8.407-3.011A11.313 11.313 0 0 0 13 7.811c-1.766 0-3.326.423-4.593.975A3.237 3.237 0 0 0 6.5 11.756V13.5h13v-1.744a3.237 3.237 0 0 0-1.907-2.969Zm-8.85 2.545c.097-.249.14-.422.985-.747A8.938 8.938 0 0 1 13 9.979c1.116 0 2.22.195 3.272.607.834.325.877.498.986.747H8.742ZM13 2.667c.596 0 1.083.487 1.083 1.083S13.596 4.833 13 4.833a1.087 1.087 0 0 1-1.083-1.083c0-.596.487-1.083 1.083-1.083ZM13 .5a3.246 3.246 0 0 0-3.25 3.25A3.246 3.246 0 0 0 13 7a3.246 3.246 0 0 0 3.25-3.25A3.246 3.246 0 0 0 13 .5Z"
        fill={fill ?? 'white'}
      />
    </svg>
  )
}

const IconNoGroup = ({ title, ...props }: Props) => {
  return (
    <svg
      width="238"
      height="179"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g fillRule="evenodd" clipRule="evenodd" fill="#7A83AB">
        <path d="M194.727 178.026 32.455 15.754 47.754.454l162.273 162.273-15.3 15.299Z" />
        <path d="M98.022 96.62c-7.723 1.616-14.788 4.005-21.069 6.742-10.71 4.76-17.453 15.47-17.453 27.172V146.5h88.402l-19.833-19.833H80.028l.084-.219c.841-2.166 1.454-3.745 8.94-6.624 8.592-3.366 17.581-5.15 26.682-5.492L98.022 96.62Zm45.346 30.047h14.605l-.125-.29c-.914-2.13-1.591-3.705-8.9-6.553a80.115 80.115 0 0 0-16.991-4.568l-20.535-20.535a101.41 101.41 0 0 1 7.578-.284c9.379 0 18.123 1.27 26.078 3.341L178.5 131.2v15.3h-15.299l-19.833-19.833Zm65.731 19.833H238v-15.569c0-8.033-4.76-15.173-12.098-18.346a68.93 68.93 0 0 0-27.569-5.752c-3.867 0-7.536.397-11.205.992 3.966 6.743 6.247 14.478 6.247 22.709v.242l15.724 15.724Zm-15.724-.425.425.425h-.425v-.425ZM140.468 77.87a29.654 29.654 0 0 0 8.282-20.62c0-16.462-13.288-29.75-29.75-29.75a29.653 29.653 0 0 0-20.62 8.282l14.053 14.053A9.875 9.875 0 0 1 119 47.333c5.454 0 9.917 4.463 9.917 9.917a9.87 9.87 0 0 1-2.502 6.567l14.053 14.053ZM92.005 44.705A29.712 29.712 0 0 0 89.25 57.25C89.25 73.712 102.538 87 119 87c4.485 0 8.735-.987 12.545-2.755l-39.54-39.54ZM59.5 77.083c0 10.909-8.925 19.834-19.833 19.834-10.909 0-19.834-8.925-19.834-19.834 0-10.908 8.925-19.833 19.834-19.833 10.908 0 19.833 8.925 19.833 19.833Zm-19.833 29.75c3.867 0 7.536.397 11.206.992-3.967 6.743-6.248 14.478-6.248 22.709V146.5H0v-15.569c0-8.033 4.76-15.173 12.098-18.346a68.93 68.93 0 0 1 27.569-5.752Zm178.5-29.75c0 10.909-8.925 19.834-19.834 19.834-10.908 0-19.833-8.925-19.833-19.834 0-10.908 8.925-19.833 19.833-19.833 10.909 0 19.834 8.925 19.834 19.833Z" />
      </g>
    </svg>
  )
}

const IconUni = ({ title, ...props }: Props) => {
  return (
    <svg
      width="27"
      height="26"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="M13.5 11.917c1.44 0 4.333.726 4.333 2.166v.174A5.724 5.724 0 0 1 13.5 16.25a5.724 5.724 0 0 1-4.334-1.993v-.174c0-1.44 2.893-2.166 4.334-2.166Zm0-1.084a2.173 2.173 0 0 1-2.167-2.166c0-1.192.975-2.167 2.167-2.167 1.191 0 2.166.975 2.166 2.167a2.173 2.173 0 0 1-2.166 2.166Zm6.5.217c0-3.932-2.871-6.717-6.5-6.717-3.63 0-6.5 2.785-6.5 6.717 0 2.535 2.112 5.893 6.5 9.902 4.387-4.009 6.5-7.367 6.5-9.902Zm-6.5-8.883c4.55 0 8.666 3.488 8.666 8.883 0 3.597-2.892 7.854-8.666 12.783-5.774-4.929-8.667-9.186-8.667-12.783 0-5.395 4.117-8.883 8.667-8.883Z"
          fill="#fff"
        />
      </g>
    </svg>
  )
}

const IconLink = ({ title, ...props }: Props) => {
  return (
    <svg
      width="20"
      height="20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <g>
        <path
          d="M15.8333 15.8333H4.16667V4.16667H10V2.5H4.16667C3.24167 2.5 2.5 3.25 2.5 4.16667V15.8333c0 .9167.74167 1.6667 1.66667 1.6667H15.8333c.9167 0 1.6667-.75 1.6667-1.6667V10h-1.6667v5.8333ZM11.6667 2.5v1.66667h2.9916L6.46667 12.3583l1.175 1.175 8.19163-8.19163v2.99166H17.5V2.5h-5.8333Z"
          fill="#fff"
        />
      </g>
    </svg>
  )
}

const IconMinus = ({ title, ...props }: Props) => {
  return (
    <svg
      width="24"
      height="24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <path stroke="#fff" strokeWidth="2" d="M19 12H5" />
    </svg>
  )
}

const IconPlus = ({ title, ...props }: Props) => {
  return (
    <svg
      width="24"
      height="24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <title>{title}</title>
      <path stroke="#fff" strokeWidth="2" d="M12 5v14M19 12H5" />
    </svg>
  )
}

export {
  IconChevron,
  IconArrowCircle,
  IconArrowSubmit,
  IconCrossReset,
  IconNote,
  IconTarget,
  IconSearch,
  IconSearchPlaceholder,
  IconGroup,
  IconNoGroup,
  IconUni,
  IconLink,
  IconMinus,
  IconPlus
}
