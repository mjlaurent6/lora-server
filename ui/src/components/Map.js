import * as React from 'react'
import {render} from 'react-dom'
import Map, {Marker} from 'react-map-gl'

import 'mapbox-gl/dist/mapbox-gl.css'
import MarkerView from './MarkerView'
import {useEffect, useState} from 'react'

const MAPBOX_TOKEN = 'pk.eyJ1IjoibWljcm9zdHVjazIiLCJhIjoiY2xjNzc5ZnR5MWYxaTNucGc3dXI1ZW9jbSJ9.oA3eGIumdRb785WUNBlLpg' // Set your mapbox token here

function MapView({sensors}) {
    const [viewState, setViewState] = useState({
        latitude: 37.8,
        longitude: -122.4,
        zoom: 14
    })

    const [long, setLong] = useState(-122.4)

    // useEffect(() => {
    //   const interval = setInterval(() => {
    //     setLong(getRandomFloat(-122.3, -122.6, 5))
    //   }, 1000)
    //   return () => clearInterval(interval)
    // }, [])

    return (
        <div>
            <Map
                {...viewState}
                onMove={evt => setViewState(evt.viewState)}
                style={{width: '50vw', height: '80vh'}}
                mapStyle="mapbox://styles/mapbox/streets-v9"
                mapboxAccessToken={MAPBOX_TOKEN}
            >
                {sensors.map(({id, long, lat, color}) => (
                    <MarkerView
                        key={id}
                        id={id}
                        long={long}
                        lat={lat}
                        color={color}
                        zoom={viewState.zoom}
                    />
                ))}
            </Map>
        </div>
    );
}

export default MapView;