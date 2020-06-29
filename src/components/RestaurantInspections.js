import React, { Component } from 'react';
import MapContainer from './map/MapContainer';
import { DataContext } from './providers/DataProvider';

class RestaurantInspections extends Component {
    static contextType = DataContext;

    render() {
        const context = this.context;
        if (context["restaurantInspections"].length === 0) {
            // TODO: handle "loading" better
            return (<div>Loading...</div>);
        }
        return (
            <div className="restaurant-inspections">
                <MapContainer data={context["restaurantInspections"]} />
            </div>
        );
    }
}

export default RestaurantInspections;