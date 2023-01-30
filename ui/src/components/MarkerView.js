/* eslint-disable react/prop-types */
import React from 'react'
import { Marker } from 'react-map-gl'

function MarkerView ({ id , long, lat, color, zoom }) {
  const size = (zoom / 16) * 30
  const strSize = String(size)
  const center = String(size / 2)
  return (
    <Marker longitude={long} latitude={lat}>
        <div>{id}</div>
        <svg height={strSize} width={strSize}>
          <circle fill={color} stroke="none" cx={center} cy={center} r={center}>
            <animate attributeName="opacity" dur="1s" values="0;1;0" repeatCount="indefinite" begin="0.1" />
          </circle>
        </svg>
      </Marker>
  )
}

export default MarkerView;
