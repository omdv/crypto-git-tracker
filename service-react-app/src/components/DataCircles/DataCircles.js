import React, { Component } from 'react'
import './DataCircles.css'

// import { scaleOrdinal } from 'd3-scale'
// import { symbol } from 'd3-shape'
// import { schemeCategory10 } from 'd3-scale-chromatic'

// export default class Points extends Component {
//   constructor(props) {
//     super(props)
//     this.colorScale = scaleOrdinal(schemeCategory10)
//   }

export default class DataCircles extends Component {
  constructor() {
    super()
    this.state = {
      onHover: false,
      hoverTicker: null
    }
    this.renderCircles.bind(this)
  }

  onItemMouseOver = (posX, posY, ticker, e) => {
    this.setState({
      onHover: true,
      hoverTicker: ticker,
      hoverX: posX,
      hoverY: posY-7
    })
  }

  onItemMouseOut = (e) => {
    this.setState({onHover: false})
  }

  renderCircles = (props) => {
    const {onHover, hoverTicker, hoverX, hoverY} = this.state
    return (coords, index) => {
      const posX = props.scales.xScale(coords[props.xAccessor])
      const posY = props.scales.yScale(coords[props.yAccessor])
      const ticker = coords['ticker']
      const circleProps = {
        cx: posX,
        cy: posY,
        r: 4,
        key: index,
        stroke: "blue",
        fill: "red"
      };
      return <g key={`group-${index}`}
          onMouseOver={this.onItemMouseOver.bind(this, posX, posY, ticker)}
          onMouseOut={this.onItemMouseOut.bind(this)}>
        <circle {...circleProps}/>
        {onHover && <text
          x={hoverX}
          y={hoverY}
          key={`text-${index}`}>{hoverTicker}</text>}
      </g>
    }
  }

  render() {
    return <g>{ this.props.data.map(this.renderCircles(this.props)) }</g>
  }
}