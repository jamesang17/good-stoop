import React, { Component } from 'react';
import MapContainer from './map/MapContainer';

class NypdComplaints extends Component {
    render() {
        return (
            <div className="nypd-complaints">
                <MapContainer />
            </div>
        );
    }
}

export default NypdComplaints;