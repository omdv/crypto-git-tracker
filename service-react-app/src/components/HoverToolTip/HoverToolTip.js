import React, { Component } from 'react'
import './HoverToolTip.css'


export default class HoverToolTip extends Component {

  render() {
    // const { readings, svgDimensions, margins, scales } = this.props
    // const { height } = svgDimensions
    const { screenPos } = this.props
    // const { xReadings, yReadings } = readings

    // define text
    const text = (<text
      x={50}
      y={50}>{screenPos.x}</text>)

    // const line = (<line 
    //   x1={xScale(xReadings)}
    //   y1={height-margins.bottom}
    //   x2={xScale(xReadings)}
    //   y2={margins.top}
    //   strokeWidth="0.5" stroke="black"/>
    // )

    // // define hover circles
    // const circles = (
    //   Object.keys(yReadings).map(key =>
    //     <circle
    //       key={"circle"+key}
    //       cx={xScale(xReadings)}
    //       cy={yScale(yReadings[key])}
    //       r="3"
    //       stroke="black"
    //       fill="none"
    //     />
    //     )
    //   )


    return (
      <g className={`HoverToolTip`}>{text}</g>
    )
  }
}
