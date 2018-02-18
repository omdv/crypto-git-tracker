import React from 'react'
import './DataCircles.css'

// import { scaleOrdinal } from 'd3-scale'
// import { symbol } from 'd3-shape'
// import { schemeCategory10 } from 'd3-scale-chromatic'

// export default class Points extends Component {
//   constructor(props) {
//     super(props)
//     this.colorScale = scaleOrdinal(schemeCategory10)
//   }

//   render() {
//     const { scales, margins, data, x_accessor, y_accessor } = this.props
//     const { xScale, yScale } = scales


//     const renderCircles = (props) => {
//       return (coords, index) => {
//         const circleProps = {
//           cx: props.scales.xScale(props.data[x_accessor]),
//           cy: props.scales.yScale(props.data[y_accessor]),
//           r: 2,
//           key: index
//         };
//         return <circle {...circleProps} />;
//       };
//     };

//   }
// }

const mouseOver = (e) => {
  console.log(e)
}

const mouseOut = (e) => {
  console.log(e)
}

const renderCircles = (props) => {
  return (coords, index) => {
    const circleProps = {
      cx: props.scales.xScale(coords[props.x_accessor]),
      cy: props.scales.yScale(coords[props.y_accessor]),
      r: 6,
      key: index,
      stroke: "blue",
      fill: "red"
    };
    return <g onMouseOver={mouseOver} onMouseOut={mouseOut} key={index}>
      <circle {...circleProps} />
      <text x={circleProps.cx} y={circleProps.cy} className="data-labels">{coords['ticker']}</text>
    </g>;
  };
};

export default (props) => {
  return <g>{ props.data.map(renderCircles(props)) }</g>
}