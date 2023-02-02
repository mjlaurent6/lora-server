import * as React from 'react'
import {render} from 'react-dom'
import Map, {Marker} from 'react-map-gl'

import 'mapbox-gl/dist/mapbox-gl.css'
import MarkerView from './MarkerView'
import {useEffect, useState} from 'react'

const MAPBOX_TOKEN = 'pk.eyJ1IjoibWljcm9zdHVjazIiLCJhIjoiY2xjNzc5ZnR5MWYxaTNucGc3dXI1ZW9jbSJ9.oA3eGIumdRb785WUNBlLpg' // Set your mapbox token here
// const MAPBOX_TOKEN = 'EMPTY' // Set your mapbox token here

function MapView({serverApi, sensors}) {
    const [viewState, setViewState] = useState({
        latitude: 37.8,
        longitude: -122.4,
        zoom: 14
    })

    const [sensorData, setSensorData] = useState(sensors);

    const [long, setLong] = useState(-122.4)

    // useEffect(() => {
    //     const interval = setInterval(() => {
    //         const fakePayload = serverApi.getBlinkingLocation()
    //         const {lat, long} = fakePayload[0];
    //         setViewState({latitude: lat, longitude: long, zoom: 14})
    //         console.log(fakePayload)
    //         setSensorData(fakePayload)
    //     }, 1000)
    //     return () => clearInterval(interval)
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
                {sensorData.map(({id, long, lat, color}) => (
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