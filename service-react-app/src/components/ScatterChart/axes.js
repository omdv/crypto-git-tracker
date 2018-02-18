import React from 'react'
import Axis from '../Axis'


export default ({ scales, margins, svgDimensions }) => {
  const { height } = svgDimensions

  const xProps = {
    orient: 'Bottom',
    scale: scales.xScale,
    translate: `translate(0, ${height - margins.bottom})`,
    tickSize: 5,
    ticks: [8]
  }

  const yProps = {
    orient: 'Left',
    scale: scales.yScale,
    translate: `translate(${margins.left}, 0)`,
    tickSize: 5,
    ticks: [8]
  }

  return (
    <g>
      <Axis {...yProps} />
      <Axis {...xProps} />
    </g>
  )
}