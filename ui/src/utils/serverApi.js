export default function ServerApi() {

    function getRandomFloat(upper, bottom){
        return (Math.random() * (bottom - upper) + upper).toFixed(1)
    }

    function getBlinkingLocation() {
        const getTime = () => new Date().toLocaleString();
        const lat = getRandomFloat(37.4, 37.9)
        const long = getRandomFloat(-122.4, -122.0)
        const fakePayload = [
            {id: '#1892', lat: lat, long: long, color: '#FF0000', timestamp: getTime()},
        ]
        return fakePayload
    }

    function getBoxesLocation() {
        const getTime = () => new Date().toLocaleString();

        const fakePayload = [
            {id: '#1892', lat: 37.8, long: -122.2, color: '#FF0000', timestamp: getTime()},
            {id: '#1351', lat: 37.7, long: -122.4, color: '#00FF00', timestamp: getTime()},
            {id: '#5125', lat: 37.8, long: -122.4, color: '#0000FF', timestamp: getTime()},
        ]
        return fakePayload
    }

    return {getBoxesLocation: getBoxesLocation, getBlinkingLocation: getBlinkingLocation}
}