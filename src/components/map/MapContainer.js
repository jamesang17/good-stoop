import React from 'react';
import { Map, Polygon, GoogleApiWrapper } from 'google-maps-react';

export const MapContainer = (props) => {

  if (!props.loaded) {
    return <div>Loading...</div>
  }
  var boundPoints = [
    { lat: 40.935594, lng: -73.868499 },
    { lat: 40.712673, lng: -73.456416 },
    { lat: 40.725579, lng: -74.547076 },
    { lat: 40.466673, lng: -74.004676 },
  ]
  var bounds = new props.google.maps.LatLngBounds();
  for (var i=0;i<boundPoints.length;i++) {
    bounds.extend(boundPoints[i]);
  }

  console.log(props)

  return (
    <div style={{width: "100vw", height: "100vh"}}>
      <Map 
        google={props.google} 
        center={{
          lat: 40.7128,
          lng: -74.0060
        }}
        zoom={4}
        bounds={bounds}
        draggable={true}
      >
      </Map>
    </div>
  )
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
})(MapContainer)