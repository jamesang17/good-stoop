import React, { Component } from 'react';
import { Map, GoogleApiWrapper, HeatMap } from 'google-maps-react';

class MapContainer extends Component {
  render() {
    const style = {
      width: "100vw",
      height: "100vh"
    };
    const boundPoints = [
      { lat: 40.935594, lng: -73.868499 },
      { lat: 40.712673, lng: -73.456416 },
      { lat: 40.725579, lng: -74.547076 },
      { lat: 40.466673, lng: -74.004676 },
    ];
    const bounds = new this.props.google.maps.LatLngBounds();
    for (var i = 0; i < boundPoints.length; i++) {
      bounds.extend(boundPoints[i]);
    }

    const data = this.props.data.filter(item => item.latitude !== "null" && item.longitude !== "null");
    const positions = data.map(item => {
      return {
        lat: item.latitude,
        lng: item.longitude
      }
    });

    console.log(positions);

    return (
      <div style={style}>
        <Map
          google={this.props.google}
          initialCenter={{
            lat: 40.7128,
            lng: -74.0060
          }}
          zoom={13}
          bounds={bounds}
          draggable={true}
        >
          <HeatMap
            opacity={1}
            positions={positions}
            radius={20}
          />
        </Map>
      </div>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  libraries: ["visualization"]
})(MapContainer)