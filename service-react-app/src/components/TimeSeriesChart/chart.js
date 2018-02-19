import React, { Component } from 'react'
import { scaleTime, scalePow } from 'd3-scale'
import { extent, bisector } from 'd3-array'

import Axes from './axes'
import Lines from '../Lines'
import HoverLine from '../HoverLine'
import Legend from '../Legend'
import Labels from '../Labels'
import ResponsiveWrapper from '../ResponsiveWrapper'

var _ = require('underscore')

class TimeSeriesChart extends Component {
  constructor() {
    super()
    this.xScale = scaleTime()
    this.yScale = scalePow()
    this.state = {
      hoverActive: false
    }
  }

  _onMouseOut(e) {
    this.setState({
      hoverActive: false
    })
  }

  _onMouseMove(e) {
    const xAccessor = this.props.xAccessor
    // helpers
    const { data } = this.props
    const categories = Object.keys(data[0]).slice(1)
    let bisectDate = bisector(function(d) { return d[xAccessor]; }).right;
    let hoverActive = true

    // initiate
    let xReadings = null
    let yReadings = []

    // find x coordinate
    let point = this.svg.createSVGPoint();
    point.x = e.clientX;
    point.y = e.clientY;
    point = point.matrixTransform(this.svg.getScreenCTM().inverse())

    // find data corresponding to x
    const selDate = this.xScale.invert(point.x)
    const dataIdx = bisectDate(data, selDate)

    // get x and y within try block
    try {
      xReadings = data[dataIdx][xAccessor]
      yReadings = _.pick(data[dataIdx], categories)
    }
    catch(err) {
      hoverActive = false
    }

    this.setState({
      xScreen: point.x,
      xReadings: xReadings,
      yReadings: yReadings,
      hoverActive: hoverActive
    })

  }

  render() {
    const { data, margins, xAccessor } = this.props
    const { hover_enabled, legend_enabled } = this.props
    const { xScreen, xReadings, yReadings, hoverActive } = this.state
    const svgDimensions = {
      width: Math.max(this.props.parentWidth, this.props.width),
      height: this.props.height
    }

    const categories = Object.keys(data[0]).slice(1)
    const dMax = (d) => categories.reduce((a,b) => a > d[b] ? a : d[b], 0);
    const yMax = (data) => data.reduce((a,b) => a > dMax(b) ? a : dMax(b));

    // define scales
    const xScale = this.xScale
      .range([margins.left, svgDimensions.width - margins.right])
      .domain(extent(data, function(d) { return d[xAccessor] }))

    const yScale = this.yScale
      .exponent(0.5)
      .range([svgDimensions.height - margins.bottom, margins.top])
      .domain([0, yMax(data)])

    return (
      <svg
      width={svgDimensions.width}
      height={svgDimensions.height}
      onMouseMove={this._onMouseMove.bind(this)}
      onMouseOut={this._onMouseOut.bind(this)}
      ref={(svg) => this.svg = svg}>
        <Axes
          scales={{ xScale, yScale }}
          margins={margins}
          svgDimensions={svgDimensions}/>
        <Lines
          scales={{ xScale, yScale }}
          margins={margins}
          data={data}
          xAccessor={xAccessor}/>
        <Labels
          margins={margins}
          width={svgDimensions.width}
          height={svgDimensions.height}
          xLabel={this.props.xLabel}
          yLabel={this.props.yLabel} />
        {(hover_enabled & hoverActive) && <HoverLine
          scales={{ xScale, yScale }}
          margins={margins}
          svgDimensions={svgDimensions}
          xScreen={xScreen}
          readings={{ xReadings, yReadings }} />}
        {legend_enabled && <Legend
          data={ data }
          hoverActive = { hoverActive }
          readings = {{ xReadings, yReadings }}
          scales={{ xScale, yScale }} />}
      </svg>
    )
  }
}

export default ResponsiveWrapper(TimeSeriesChart)
