import React from 'react'
import Axis from '../Axis'
import TimeAxis from '../TimeAxis'
import { timeMonth } from 'd3-time'


export default ({ scales, margins, svgDimensions }) => {
  const { height } = svgDimensions

  const xProps = {
    orient: 'Bottom',
    scale: scales.xScale,
    translate: `translate(0, ${height - margins.bottom})`,
    tickSize: 5,
    ticks: timeMonth,
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
      <TimeAxis {...xProps} />
      <Axis {...yProps} />
    </g>
  )
}
