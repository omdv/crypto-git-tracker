import React, { Component } from 'react'
import { scaleOrdinal } from 'd3-scale'
import { schemeCategory10 } from 'd3-scale-chromatic'

import './Legend.css'

const legendLineLength = 20
const textLineHeight = 15
const margin = {top: 25, left: 10}

export default class Legend extends Component {
  constructor(props) {
    super(props)
    this.colorScale = scaleOrdinal(schemeCategory10)
  }

  render() {
    const { data, scales, readings, hoverActive } = this.props
    const { xReadings, yReadings } = readings
    const { xScale } = scales

    const coins = Object.keys(data[0]).slice(1)

    // define texts for legend
    const legend_labels = (
      coins.map((coin,i) =>
      {
        const xPos = xScale(data[0].date) + margin.left
        const yPos = margin.top + textLineHeight * (i + 1)
        return <text
          key={'text' + i}
          transform={"translate(" + xPos + "," + yPos + ")"}
          x="3"
          dy="0.35em"
          fontFamily="sans-serif"
          fontSize="10px">{coin}</text>
      }
      )
    )
    
    // return xReading
    const xReadingxPos = xScale(data[0].date) + margin.left
    const xReadingyPos = margin.top
    const date_reading = <text
          transform={"translate(" + xReadingxPos + "," + xReadingyPos + ")"}
          x="3"
          dy="0.35em"
          fontFamily="sans-serif"
          fontSize="10px">{hoverActive && xReadings.toDateString()}</text>


    // define readings for legend
    const legend_readings = (
      coins.map((coin,i) =>
      {
        const xPos = xScale(data[0].date) + margin.left + legendLineLength + 40 + 5
        const yPos = margin.top + textLineHeight * (i + 1)
        const reading = hoverActive && yReadings[coin].toFixed(2)
        return <text
          key={'text' + i}
          transform={"translate(" + xPos + "," + yPos + ")"}
          x="3"
          dy="0.35em"
          fontFamily="sans-serif"
          fontSize="10px">{reading}</text>
      }
      )
    )

    // define short lines for legend
    const legend_lines = (
      coins.map((coin,i) =>
      {
        const xPos = xScale(data[0].date) + margin.left + 40
        const yPos = margin.top + textLineHeight * (i + 1)
        return <line
          key={'legend_line_'+i}
          x1={xPos}
          x2={xPos+legendLineLength}
          y1={yPos}
          y2={yPos}
          stroke={this.colorScale(i)}
        />
      }
      )
    )

    return (
      <g className={`Legend`}>{legend_labels}{legend_lines}{legend_readings}{date_reading}</g>
    )
  }
}
