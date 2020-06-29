import React, { Component } from 'react';
import MapContainer from './map/MapContainer';
import { DataContext } from './providers/DataProvider';

class NypdComplaints extends Component {
    static contextType = DataContext;

    render() {
        const context = this.context;
        if (context["nypdComplaints"].length === 0) {
            // TODO: handle "loading" better
            return (<div>Loading...</div>);
        }
        return (
            <div className="nypd-complaints">
                <MapContainer data={context["nypdComplaints"]} />
            </div>
        );
    }
}

export default NypdComplaints;