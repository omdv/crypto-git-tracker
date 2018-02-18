import React, { Component } from 'react'
import { scaleLinear, scaleTime, scalePow, scaleLog } from 'd3-scale'
import { extent, bisector } from 'd3-array'

import Axes from './axes'
import DataCircles from '../DataCircles'
import HoverLine from '../HoverLine'
import Legend from '../Legend'
import ResponsiveWrapper from '../ResponsiveWrapper'

import './chart.css'

var _ = require('underscore')

class ScatterChart extends Component {
  constructor() {
    super()
    this.xScale = scaleLinear()
    this.yScale = scaleLog()
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
    const { x_accessor, y_accessor, data } = this.props
    // helpers
    let bisectX = bisector(function(d) { return d[x_accessor]; }).right;
    let bisectY = bisector(function(d) { return d[y_accessor]; }).top;

    let hoverActive = true

    // initiate
    let xReadings = null
    let yReadings = null

    // // find x coordinate
    // let point = this.svg.createSVGPoint();
    // point.x = e.clientX;
    // point.y = e.clientY;
    // point = point.matrixTransform(this.svg.getScreenCTM().inverse())

    // // find data corresponding to x
    // const selDate = this.xScale.invert(point.x)
    // const dataIdx = bisectDate(data, selDate)

    // // get x and y within try block
    // try {
    //   xReadings = data[dataIdx][x_accessor]
    //   yReadings = _.pick(data[dataIdx], categories)
    // }
    // catch(err) {
    //   hoverActive = false
    // }

    // this.setState({
    //   xScreen: point.x,
    //   xReadings: xReadings,
    //   yReadings: yReadings,
    //   hoverActive: hoverActive
    // })

  }

  render() {
    const { data, margins, x_accessor, y_accessor } = this.props
    const { hover_enabled, legend_enabled } = this.props
    const { xScreen, xReadings, yReadings, hoverActive } = this.state
    const svgDimensions = {
      width: Math.max(this.props.parentWidth, this.props.width),
      height: this.props.height
    }

    // define scales
    const xScale = this.xScale
      .range([margins.left, svgDimensions.width - margins.right])
      .domain(extent(data, function(d) { return d[x_accessor] }))
    
    const yScale = this.yScale
      .range([svgDimensions.height - margins.bottom, margins.top])
      .domain(extent(data, function(d) { return d[y_accessor] }))

    return (
      <svg
      width={svgDimensions.width}
      height={svgDimensions.height}
      onMouseMove={this._onMouseMove.bind(this)}
      onMouseOut={this._onMouseOut.bind(this)}
      ref={(svg) => this.svg = svg}>
        <Axes
          scales={{ xScale, yScale }}
          margins={ margins }
          svgDimensions={ svgDimensions }/>
        <DataCircles
          scales={{ xScale, yScale }}
          margins={ margins }
          data={ data }
          x_accessor={ x_accessor }
          y_accessor={ y_accessor }/>
      </svg>
    )
  }
}

export default ResponsiveWrapper(ScatterChart)
