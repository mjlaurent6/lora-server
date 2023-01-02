import * as React from 'react';
// import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import ReactMapboxGl, { Layer, Feature } from 'react-mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import {useEffect, useRef, useState} from "react";
mapboxgl.accessToken = 'pk.eyJ1IjoibWljcm9zdHVjazIiLCJhIjoiY2xjNzc5ZnR5MWYxaTNucGc3dXI1ZW9jbSJ9.oA3eGIumdRb785WUNBlLpg';
export default function Map() {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(12.550343);
    const [lat, setLat] = useState(55.665957);
    const [zoom, setZoom] = useState(8);

    useEffect(() => {
        if (map.current) return; // initialize map only once
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [lng, lat],
            zoom: zoom
        });
    });

    return (<div ref={mapContainer} className="map-container" />)
}