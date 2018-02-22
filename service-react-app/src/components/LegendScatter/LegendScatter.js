import React from 'react'

const LegendScatter = (props) => {
      const circlePos = {
        cx: 0,
        cy: 0,
        r: 4,
        stroke: "blue",
        fill: "rgb(23, 190, 207)"
      };
      const circleNeg = {
        cx: 0,
        cy: 15,
        r: 4,
        stroke: "blue",
        fill: "rgb(214, 39, 40)"
      };

      return <g transform={`translate (${props.xPos} ${props.yPos})`}>
        <circle {...circlePos}/>
        <text dx="10" dy="4" fontFamily="sans-serif"
          fontSize="10px">{`top 10%`}</text>
        <circle {...circleNeg}/>
        <text dx="10" dy="19" fontFamily="sans-serif"
          fontSize="10px">{`bottom 10%`}</text>
      </g>
}

export default LegendScatter