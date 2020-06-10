import React, { Component } from 'react';
import MapContainer from './map/MapContainer';

class RestaurantInspections extends Component {
    render() {
        return (
            <div className="restaurant-inspections">
                <MapContainer />
            </div>
        );
    }
}

export default RestaurantInspections;