import React, { Component } from 'react';
import MapContainer from './map/MapContainer';
import { DataContext } from './providers/DataProvider';

class RestaurantInspections extends Component {
    static contextType = DataContext;

    render() {
        const context = this.context;

        console.log("Context");
        console.log(context);
        
        return (
            <div className="restaurant-inspections">
                <MapContainer />
            </div>
        );
    }
}

export default RestaurantInspections;