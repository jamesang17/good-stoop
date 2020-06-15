import React, { useState, useEffect, } from 'react';
import axios from 'axios';

export const DataContext = React.createContext();

export const DataProvider = ({ children }) => {
  const [state, setState] = useState({
    nycBoundaries: [],
    buildingComplaints: [],
    nypdComplaints: [],
    restaurantInspections: []
  })

  const loadData = () => {
    const boroughPromise = axios.get('/api/borough_boundaries');
    const buildingPromise = axios.get('/api/building_complaint_results');
    const nypdPromise = axios.get('/api/nypd_complaint_results');
    const restaurantPromise = axios.get('/api/restaurant_inspection_results');

    Promise.all([boroughPromise, buildingPromise, nypdPromise, restaurantPromise])
      .then(values => {
        const boroughData = values[0].data.data;
        const buildingData = values[1].data.data;
        const nypdData = values[2].data.data;
        const restaurantData = values[3].data.data;

        setState({
          nycBoundaries: boroughData,
          buildingComplaints: buildingData,
          nypdComplaints: nypdData,
          restaurantInspections: restaurantData
        });
      })
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <DataContext.Provider value={state}>
      {children}
    </DataContext.Provider>
  )
}