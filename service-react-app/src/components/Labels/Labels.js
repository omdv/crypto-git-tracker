import React from 'react'

const renderLabels = (props) => {
  const yPos = (props.height-props.margins.top-props.margins.bottom)/2+props.margins.top
  const xPos = 12
  return <g>
    {props.xLabel && <text
      x={props.width/2}
      y={props.height-props.margins.bottom/2}
      dx={props.margins.left/2}
      dy={10}
      textAnchor={'middle'}
      className={`Axis-Labels-xLabel`}>{props.xLabel}</text>}
 	{props.yLabel && <text
      x={xPos}
      y={yPos}
      textAnchor={'middle'}
      className={`Axis-Labels-yLabel`}
      transform={`rotate(270,${xPos},${yPos})`}
      >{props.yLabel}</text>}
  </g>
}

export default (props) => {
  return renderLabels(props)
}