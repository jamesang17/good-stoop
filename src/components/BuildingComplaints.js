import React, { Component } from 'react';
import MapContainer from './map/MapContainer';
import { DataContext } from './providers/DataProvider';

class BuildingComplaints extends Component {
    static contextType = DataContext;

    render() {
        const context = this.context;
        if (context["buildingComplaints"].length === 0) {
            // TODO: handle "loading" better
            return (<div>Loading...</div>);
        }
        return (
            <div className="building-complaints">
                <MapContainer data={context["buildingComplaints"]} />
            </div>
        );
    }
}

export default BuildingComplaints;