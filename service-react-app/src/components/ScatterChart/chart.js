import React, { Component } from 'react'
import { scaleLinear, scaleLog } from 'd3-scale'
import { extent } from 'd3-array'

import Axes from './axes'
import DataCircles from '../DataCircles'
import Labels from '../Labels'
import ResponsiveWrapper from '../ResponsiveWrapper'

import './chart.css'

class ScatterChart extends Component {

  xScale = scaleLinear()
  yScale = scaleLog()

  render() {
    const { data, margins, xAccessor, yAccessor } = this.props
    const svgDimensions = {
      width: Math.max(this.props.parentWidth, this.props.width),
      height: this.props.height
    }

    // define scales
    const xScale = this.xScale
      .range([margins.left, svgDimensions.width - margins.right])
      .domain(extent(data, function(d) { return d[xAccessor] }))
    
    const yScale = this.yScale
      .range([svgDimensions.height - margins.bottom, margins.top])
      .domain(extent(data, function(d) { return d[yAccessor] }))

    return (
      <svg
      width={svgDimensions.width}
      height={svgDimensions.height}
      ref={(svg) => this.svg = svg}>
        <Axes
          scales={{ xScale, yScale }}
          margins={ margins }
          svgDimensions={ svgDimensions }/>
        <DataCircles
          scales={{ xScale, yScale }}
          margins={ margins }
          data={ data }
          xAccessor={ xAccessor }
          yAccessor={ yAccessor }
          outlierAccessorPos = { this.props.outlierAccessorPos }
          outlierAccessorNeg = { this.props.outlierAccessorNeg } />
        <Labels
          margins={margins}
          width={svgDimensions.width}
          height={svgDimensions.height}
          xLabel={this.props.xLabel}
          yLabel={this.props.yLabel} />
      </svg>
    )
  }
}

export default ResponsiveWrapper(ScatterChart)
