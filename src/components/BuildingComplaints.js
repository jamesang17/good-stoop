import React, { Component } from 'react';
import MapContainer from './map/MapContainer';

class BuildingComplaints extends Component {
    render() {
        return (
            <div className="building-complaints">
                <MapContainer />
            </div>
        );
    }
}

export default BuildingComplaints;