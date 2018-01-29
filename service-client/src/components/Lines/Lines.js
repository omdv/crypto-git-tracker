import React, { Component } from 'react'
import { scaleOrdinal, schemeCategory10 } from 'd3-scale'
import { line, curveBasis } from 'd3-shape'

export default class Lines extends Component {
  constructor(props) {
    super(props)
    this.colorScale = scaleOrdinal(schemeCategory10)
  }

  render() {
    const { scales, margins, data } = this.props
    const { xScale, yScale } = scales

    const coins = Object.keys(data[0]).slice(1)

    // define lines for each coin
    const lines = coins.map((coin, i) => line()
      // .curve(curveBasis)
      .x(function(d) { return xScale(d.date) })
      .y(function(d) { return yScale(d[coin]) }))

    // define paths
    const paths = (
      lines.map((line,i) =>
        <path
          key={'path' + i}
          d={line(data)}
          stroke={this.colorScale(i)}
          fill="none"
        />
        )
      )

    const translation = 'translate(' + margins.left + ',' + margins.top + ')'

    return (
      <g translate={translation}>{paths}</g>
    )
  }
}
