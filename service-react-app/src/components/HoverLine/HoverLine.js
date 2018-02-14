import React, { Component } from 'react'
import { line, curveBasis } from 'd3-shape'

import './HoverLine.css'


export default class HoverLine extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    const { xScreen, readings, svgDimensions, margins, scales } = this.props
    const { height } = svgDimensions
    const { xScale, yScale } = scales
    const { xReadings, yReadings } = readings

    // define line
    const line = (<line 
      x1={xScale(xReadings)}
      y1={height-margins.bottom}
      x2={xScale(xReadings)}
      y2={margins.top}
      strokeWidth="0.5" stroke="black"/>
    )

    // define hover circles
    const circles = (
      Object.keys(yReadings).map(key =>
        <circle
          key={"circle"+key}
          cx={xScale(xReadings)}
          cy={yScale(yReadings[key])}
          r="3"
          stroke="black"
          fill="none"
        />
        )
      )


    return (
      <g className={`HoverLine`}>{line}{circles}</g>
    )
  }
}
