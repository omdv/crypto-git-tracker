import React, { Component } from 'react'
import { scaleOrdinal } from 'd3-scale'
import { line, curveBasis } from 'd3-shape'
import { schemeCategory10 } from 'd3-scale-chromatic'

export default class Lines extends Component {
  constructor(props) {
    super(props)
    this.colorScale = scaleOrdinal(schemeCategory10)
  }

  render() {
    const { scales, margins, data, x_accessor } = this.props
    const { xScale, yScale } = scales

    const items = Object.keys(data[0]).slice(1)

    // define lines for each item
    const lines = items.map((item, i) => line()
      // .curve(curveBasis)
      .x(function(d) { return xScale(d[x_accessor]) })
      .y(function(d) { return yScale(d[item]) }))

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
