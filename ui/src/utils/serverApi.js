export default function ServerApi() {
    function getBoxesLocation() {
        const getTime = () => new Date().toLocaleString();

        const fakePayload = [
            {id: '#1892', lat: 37.8, long: -122.2, color: '#FF0000', timestamp: getTime()},
            {id: '#1351', lat: 37.7, long: -122.4, color: '#00FF00', timestamp: getTime()},
            {id: '#5125', lat: 37.8, long: -122.4, color: '#0000FF', timestamp: getTime()},
        ]
        return fakePayload
    }

    return {getBoxesLocation: getBoxesLocation}
}