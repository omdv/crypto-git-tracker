import React, { Component } from 'react'
import scaleOrdinal from 'd3-scale/src/ordinal'
import line from 'd3-shape/src/line'
import schemeCategory10 from 'd3-scale-chromatic/src/categorical/category10'

export default class Lines extends Component {
  constructor(props) {
    super(props)
    this.colorScale = scaleOrdinal(schemeCategory10)
  }

  render() {
    const { scales, margins, data, xAccessor } = this.props
    const { xScale, yScale } = scales

    const items = Object.keys(data[0]).slice(1)

    // define lines for each item
    const lines = items.map((item, i) => line()
      // .curve(curveBasis)
      .x(function(d) { return xScale(d[xAccessor]) })
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
